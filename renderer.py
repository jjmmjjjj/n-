import pygame

WIDTH = 1280
HEIGHT = 720

FOV = 500


def project(x, y, z):

    if z <= 1:
        return None

    scale = FOV / z

    sx = int(x * scale + WIDTH / 2)
    sy = int(y * scale + HEIGHT / 2)

    return sx, sy, scale


def draw_axis(screen, camera):

    axis_size = 2000

    axis_lines = [

        # X축
        (
            (-axis_size, 0, 0),
            (axis_size, 0, 0),
            (255, 0, 0)
        ),

        # Y축
        (
            (0, -axis_size, 0),
            (0, axis_size, 0),
            (0, 255, 0)
        ),

        # Z축
        (
            (0, 0, -axis_size),
            (0, 0, axis_size),
            (0, 100, 255)
        )
    ]

    for start, end, color in axis_lines:

        sx, sy, sz = camera.world_to_camera(*start)
        ex, ey, ez = camera.world_to_camera(*end)

        p1 = project(sx, sy, sz)
        p2 = project(ex, ey, ez)

        if p1 and p2:

            x1, y1, _ = p1
            x2, y2, _ = p2

            pygame.draw.line(
                screen,
                color,
                (x1, y1),
                (x2, y2),
                2
            )


def draw_bodies(screen, bodies, camera):

    render_list = []

    for body in bodies:

        cx, cy, cz = camera.world_to_camera(
            body.x,
            body.y,
            body.z
        )

        render_list.append(
            (cz, body, cx, cy)
        )

    render_list.sort(
        key=lambda item: item[0],
        reverse=True
    )

    for cz, body, cx, cy in render_list:

        
        # 궤적
        trail_points = []

        for tx, ty, tz in body.trail:

            px, py, pz = camera.world_to_camera(
                tx,
                ty,
                tz
            )

            projected = project(
                px,
                py,
                pz
            )

            if projected:

                sx, sy, _ = projected

                trail_points.append(
                    (sx, sy)
                )

        if len(trail_points) >= 2:

            pygame.draw.lines(
                screen,
                body.color,
                False,
                trail_points,
                1
            )

        
        # 본체
        projected = project(
            cx,
            cy,
            cz
        )

        if not projected:
            continue

        sx, sy, scale = projected

        radius = max(
            3,
            int(body.mass * scale * 0.00001)
        )

        pygame.draw.circle(
            screen,
            body.color,
            (sx, sy),
            radius
        )