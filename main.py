import click
import json
import os
import numpy as np
from robot_model import RobotConfig
from optimizer import TrajectoryOptimizer
from plotter import plot_trajectory
from validator import validate_trajectory
from export import write_controller_file

@click.command()
@click.option('--config', '-c', required=True, type=click.Path(exists=True), help='Path to the .chor configuration file.')
@click.option('--waypoints', '-w', required=True, type=click.Path(exists=True), help='Path to waypoints JSON file.')
@click.option('--output', '-o', default='output.traj', help='Output trajectory file path.')
@click.option('--samples', '-s', default=10, help='Samples per segment.')
@click.option('--accuracy-weight', '-a', default=0.0, type=float, help='Smoothness/accuracy weight (0 = pure time-optimal).')
@click.option('--validate', is_flag=True, help='Run validation report on the generated trajectory.')
@click.option('--export-format', default='none', type=click.Choice(['none', 'controller']), help='Export format for controller consumption.')
@click.option('--controller-dt', default=0.02, type=float, help='Fixed timestep for controller export (seconds).')
@click.option('--plot', is_flag=True, help='Plot the resulting trajectory.')
def main(config, waypoints, output, samples, accuracy_weight, validate, export_format, controller_dt, plot):
    """
    FLL Trajectory Optimizer CLI.
    Generates time-optimal trajectories for Lego robots.
    """
    click.echo(f"Loading config from {config}...")
    with open(config, 'r') as f:
        config_data = json.load(f)
    
    robot_cfg = RobotConfig(config_data)
    optimizer = TrajectoryOptimizer(robot_cfg)
    
    click.echo(f"Loading waypoints from {waypoints}...")
    with open(waypoints, 'r') as f:
        wp_data = json.load(f)
    
    # Expected wp_data: list of objects with x, y, and optionally heading
    # or list of lists [x, y, heading]
    wps = []
    for item in wp_data:
        if isinstance(item, dict):
            wps.append((item['x'], item['y'], item.get('heading')))
        else:
            # Assume [x, y, heading]
            wps.append((item[0], item[1], item[2] if len(item) > 2 else None))
            
    click.echo(f"Optimizing trajectory through {len(wps)} waypoints (accuracy_weight={accuracy_weight})...")
    samples_data = optimizer.solve(wps, num_samples_per_segment=samples, accuracy_weight=accuracy_weight)
    
    # Construct Choreo-like output
    result = {
        "name": os.path.basename(output).split('.')[0],
        "version": 3,
        "trajectory": {
            "config": config_data.get("config", {}),
            "samples": samples_data
        }
    }
    
    with open(output, 'w') as f:
        json.dump(result, f, indent=1)
    
    click.echo(f"Successfully saved trajectory to {output}")

    if validate:
        validate_trajectory(output, config)

    if export_format == 'controller':
        ctrl_output = os.path.splitext(output)[0] + '_controller.json'
        write_controller_file(output, ctrl_output, target_dt=controller_dt,
                              track_width=robot_cfg.track_width)

    if plot:
        plot_trajectory(samples_data, waypoints=wps,
                        title=f"Trajectory: {os.path.basename(output)}")

if __name__ == '__main__':
    main()
