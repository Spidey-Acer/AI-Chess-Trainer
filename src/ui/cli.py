"""
Command-Line Interface for AI Chess Trainer
"""

import click
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from pathlib import Path

from ..core import ChessEngine, GameAnalyzer
from ..ai import ChessTrainer, LLMIntegration
from ..data import GameManager, Database

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    AI Chess Trainer - Improve your chess with AI-powered analysis and feedback.
    """
    pass


@cli.command()
@click.argument("pgn_file", type=click.Path(exists=True))
@click.option("--depth", default=20, help="Analysis depth (default: 20)")
@click.option("--save", is_flag=True, help="Save analysis to database")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed analysis")
def analyze(pgn_file, depth, save, verbose):
    """
    Analyze a chess game from a PGN file.

    Example: chess-trainer analyze game.pgn --depth 20 --save
    """
    console.print(f"\n[bold blue]Analyzing game:[/bold blue] {pgn_file}\n")

    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Analyzing...", total=100)

            # Initialize trainer
            with ChessTrainer() as trainer:
                progress.update(task, advance=20)

                # Analyze game
                result = trainer.analyze_game_with_feedback(pgn_file)
                progress.update(task, advance=60)

                # Display results
                analysis = result["analysis"]
                feedback = result["feedback"]

                progress.update(task, advance=20)

        # Display game info
        metadata = analysis["metadata"]
        console.print(Panel(
            f"[bold]{metadata['white']}[/bold] vs [bold]{metadata['black']}[/bold]\n"
            f"Result: {metadata['result']}\n"
            f"Event: {metadata['event']} ({metadata['date']})",
            title="Game Information"
        ))

        # Display statistics
        _display_statistics(analysis["statistics"], feedback)

        # Display critical positions
        if verbose:
            _display_critical_positions(result, trainer)

        # Display AI summary
        console.print("\n[bold cyan]AI Summary:[/bold cyan]")
        console.print(Panel(feedback["ai_summary"]))

        # Save to database if requested
        if save:
            with Database() as db:
                game_id = db.save_game_analysis(
                    metadata,
                    analysis["statistics"]["white"],
                    analysis["statistics"]["black"],
                    analysis,
                    pgn_file,
                )
            console.print(f"\n[green]✓[/green] Analysis saved to database (ID: {game_id})")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.option("--type", "position_type",
              type=click.Choice(["mistakes", "critical", "tactical"]),
              default="mistakes",
              help="Type of training positions")
@click.option("--count", default=5, help="Number of positions (default: 5)")
@click.argument("pgn_file", type=click.Path(exists=True), required=False)
def train(position_type, count, pgn_file):
    """
    Start an interactive training session.

    Example: chess-trainer train --type tactical --count 10 game.pgn
    """
    console.print(f"\n[bold blue]Starting Training Session[/bold blue]\n")

    if not pgn_file:
        console.print("[yellow]No PGN file provided. Please provide a game to train from.[/yellow]")
        return

    try:
        with ChessTrainer() as trainer:
            # Analyze game to extract positions
            console.print("Preparing training positions...")
            with GameAnalyzer(trainer.engine) as analyzer:
                game_analysis = analyzer.analyze_game_from_pgn(pgn_file)

            # Generate training positions
            positions = trainer.generate_training_positions(
                game_analysis,
                position_type=position_type,
                count=count
            )

            if not positions:
                console.print(f"[yellow]No {position_type} positions found in this game.[/yellow]")
                return

            console.print(f"\n[green]Found {len(positions)} training positions![/green]\n")

            # Interactive training loop
            correct_count = 0
            for i, pos in enumerate(positions, 1):
                console.print(f"\n[bold]Position {i}/{len(positions)}[/bold]")
                console.print(f"FEN: {pos.get('fen', pos.get('fen_before', ''))}")

                # Get user move
                move = click.prompt("\nYour move (UCI notation, or 'skip')")

                if move.lower() == 'skip':
                    console.print(f"[yellow]Best move was: {pos.get('best_move')}[/yellow]")
                    continue

                # Check solution
                result = trainer.check_move_solution(
                    pos.get('fen', pos.get('fen_before', '')),
                    move,
                    str(pos.get('best_move', ''))
                )

                if result["correct"]:
                    console.print(f"[green]✓ {result['message']}[/green]")
                    correct_count += 1
                else:
                    console.print(f"[red]✗ {result['message']}[/red]")

            # Summary
            console.print(f"\n[bold]Training Complete![/bold]")
            console.print(f"Score: {correct_count}/{len(positions)} ({correct_count/len(positions)*100:.1f}%)")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.option("--player", help="Filter by player name")
@click.option("--limit", default=10, help="Number of games to show")
def stats(player, limit):
    """
    View your training statistics and progress.

    Example: chess-trainer stats --player "John Doe"
    """
    console.print("\n[bold blue]Training Statistics[/bold blue]\n")

    try:
        with Database() as db:
            if player:
                # Player-specific statistics
                stats_data = db.get_player_statistics(player)

                if not stats_data or stats_data.get("games_count", 0) == 0:
                    console.print(f"[yellow]No games found for player: {player}[/yellow]")
                    return

                console.print(Panel(
                    f"Games Analyzed: {stats_data['games_count']}\n"
                    f"Average Accuracy: {stats_data['avg_accuracy']:.1f}%\n"
                    f"Total Blunders: {stats_data['total_blunders']}\n"
                    f"Total Mistakes: {stats_data['total_mistakes']}\n"
                    f"Total Inaccuracies: {stats_data['total_inaccuracies']}\n"
                    f"Avg. Centipawn Loss: {stats_data['avg_acpl']:.1f}",
                    title=f"Statistics for {player}"
                ))

            # Show recent games
            games = db.get_game_history(player, limit)

            if games:
                table = Table(title="Recent Games")
                table.add_column("Date", style="cyan")
                table.add_column("White", style="white")
                table.add_column("Black", style="white")
                table.add_column("Result", style="yellow")

                for game in games:
                    table.add_row(
                        game["date"],
                        game["white_player"],
                        game["black_player"],
                        game["result"]
                    )

                console.print("\n")
                console.print(table)
            else:
                console.print("[yellow]No games in database yet.[/yellow]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.argument("directory", type=click.Path(exists=True), required=False)
def list_games(directory):
    """
    List all PGN files in a directory.

    Example: chess-trainer list-games ./my_games
    """
    if not directory:
        directory = "./data/sample_games"

    console.print(f"\n[bold blue]PGN Files in {directory}[/bold blue]\n")

    game_manager = GameManager()
    games = game_manager.list_games(directory)

    if not games:
        console.print("[yellow]No PGN files found.[/yellow]")
        return

    table = Table()
    table.add_column("#", style="cyan")
    table.add_column("File", style="white")
    table.add_column("White", style="white")
    table.add_column("Black", style="white")
    table.add_column("Result", style="yellow")

    for i, game_path in enumerate(games, 1):
        try:
            info = game_manager.get_game_info(game_path)
            table.add_row(
                str(i),
                os.path.basename(game_path),
                info["white"],
                info["black"],
                info["result"]
            )
        except Exception:
            table.add_row(str(i), os.path.basename(game_path), "?", "?", "?")

    console.print(table)


def _display_statistics(statistics, feedback):
    """Display game statistics in a table."""
    table = Table(title="Game Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("White", style="white")
    table.add_column("Black", style="white")

    white = statistics["white"]
    black = statistics["black"]
    white_fb = feedback["white"]
    black_fb = feedback["black"]

    table.add_row("Accuracy", f"{white['accuracy']:.1f}%", f"{black['accuracy']:.1f}%")
    table.add_row("Assessment", white_fb["overall_assessment"], black_fb["overall_assessment"])
    table.add_row("Blunders", str(white["blunders"]), str(black["blunders"]))
    table.add_row("Mistakes", str(white["mistakes"]), str(black["mistakes"]))
    table.add_row("Inaccuracies", str(white["inaccuracies"]), str(black["inaccuracies"]))
    table.add_row("Avg. CP Loss", f"{white['average_centipawn_loss']:.1f}", f"{black['average_centipawn_loss']:.1f}")

    console.print("\n")
    console.print(table)


def _display_critical_positions(result, trainer):
    """Display critical positions and mistakes."""
    feedback = result["feedback"]

    for player in ["white", "black"]:
        worst = feedback[player]["worst_mistakes"]
        if worst:
            console.print(f"\n[bold {player}]Worst Mistakes for {player.title()}:[/bold {player}]")
            for mistake in worst[:3]:
                console.print(f"  Move {mistake['move_number']}: {mistake['move']} "
                             f"({mistake['mistake_type']}, -{mistake['eval_loss']} cp)")
                console.print(f"  Better: {mistake['best_move']}")


if __name__ == "__main__":
    cli()
