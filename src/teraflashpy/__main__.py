import typer

from teraflashpy.commands import Command

app = typer.Typer()


@app.command()
def command(command: Command = typer.Argument()) -> None:
    print(command)


# @app.command()
# def main(command: Command = typer.Argument(default="SYSTEM : STOP", help="Model to choose")) -> None:
#     state = SystemState(
#         status=SystemStatus.On,
#         laser_state=LaserState(
#             status=LaserStatus.Off,
#             pump_current=50,
#             transfer_status=TransferStatus.Block,
#             tia_status=TransImpedanceAmplifierStatus.Medium,
#         ),
#     )
#     result, state, value = run(state, Command.SystemTellStatus, NoInput)
#     print(state)


if __name__ == "__main__":
    app()
