def get_points_from_csv(file_path: str) -> list:
    """Return 2D image points from csv file.

    Args:
        file_path (str): csv file path

    Returns:
        list: 2D image points [[x1, y1], [x2, y2], ...]
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
        points = [
            list(map(lambda x: int(float(x)), line.strip().split(",")))
            for line in lines
        ]

    return points
