#!/usr/bin/env python3
"""Brainlife app: Run VAMEPipeline on a list of NWB pose-estimation files."""

import json
from pathlib import Path

from vame.pipeline import VAMEPipeline


def resolve_nwb_files(config):
    """Read NWB file paths from Brainlife's `neuro/nwb` (multi) input slot."""
    nwb = config.get("nwb")
    if not nwb:
        raise ValueError("config['nwb'] is missing — expected a list of NWB file paths")
    if isinstance(nwb, str):
        nwb = [nwb]
    return [Path(p) for p in nwb]


def build_vame_config_kwargs(config):
    """Collect curated config fields forwarded to VAMEPipeline(config_kwargs=...)."""
    kwargs = {}
    for key in ("n_clusters", "max_epochs", "pose_confidence"):
        value = config.get(key)
        if value is not None:
            kwargs[key] = value
    seg = config.get("segmentation_algorithm")
    if seg is not None:
        kwargs["segmentation_algorithms"] = [seg]
    return kwargs


def build_preprocessing_kwargs(config):
    """Collect curated config fields forwarded to pipeline.preprocessing()."""
    kwargs = {}
    for key in (
        "centered_reference_keypoint",
        "orientation_reference_keypoint",
        "run_lowconf_cleaning",
        "run_egocentric_alignment",
        "run_outlier_cleaning",
        "run_savgol_filtering",
        "run_rescaling",
    ):
        value = config.get(key)
        if value is not None:
            kwargs[key] = value
    return kwargs


def write_product_json(project_dir, sessions):
    summary = (
        f"Project: {project_dir.name}\n"
        f"Sessions: {len(sessions)}\n"
        + "\n".join(f"  - {s}" for s in sessions)
    )
    product = {
        "brainlife": [
            {"type": "text", "name": "VAME run summary", "value": summary},
        ],
        "project_name": project_dir.name,
        "sessions": sessions,
    }
    Path("product.json").write_text(json.dumps(product, indent=2))


def main():
    with open("config.json") as f:
        config = json.load(f)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    nwb_files = resolve_nwb_files(config)
    print(f"Resolved {len(nwb_files)} NWB file(s)")

    project_name = config.get("project_name", "vame_project")

    pipeline = VAMEPipeline(
        project_name=project_name,
        poses_estimations=[str(p) for p in nwb_files],
        source_software="NWB",
        working_directory=str(output_dir),
        processing_module_key=config.get("processing_module_key", "behavior"),
        pose_estimation_key=config.get("pose_estimation_key", "PoseEstimation"),
        config_kwargs=build_vame_config_kwargs(config),
    )

    print("Running VAME pipeline...")
    pipeline.run_pipeline(preprocessing_kwargs=build_preprocessing_kwargs(config))

    print("Generating figures...")
    pipeline.visualize_preprocessing(show_figure=False, save_to_file=True)
    pipeline.visualize_model_losses(show_figure=False, save_to_file=True)
    pipeline.visualize_umap(show_figure="none", save_to_file=True)

    project_dir = output_dir / project_name
    sessions = [p.stem for p in nwb_files]
    write_product_json(project_dir, sessions)

    print(f"\nDone. VAME project at {project_dir}")


if __name__ == "__main__":
    main()
