import pygame
import math

import physics

from body import Body
from physics import update_physics

from renderer import (
    draw_bodies,
    draw_axis,
    WIDTH,
    HEIGHT
)

from camera import Camera

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "3D N-Body Simulator"
)

clock = pygame.time.Clock()

camera = Camera()

bodies = []

show_axis = True
show_creator = False


# 생성 UI

input_values = {

    "x": "0",
    "y": "0",
    "z": "0",

    "vx": "0",
    "vy": "0",
    "vz": "0",

    "mass": "120",

    "r": "255",
    "g": "255",
    "b": "255"

}

fields = list(input_values.keys())

selected_field = 0


# 물체 생성 함수

def create_body(
    x, y, z,
    vx, vy, vz,
    mass,
    color
):

    bodies.append(

        Body(
            x=x,
            y=y,
            z=z,

            vx=vx,
            vy=vy,
            vz=vz,

            mass=mass,

            color=color
        )

    )


# 초기 3체 설정

create_body(

    x=20,  #x 좌표
    y=-20, #y 좌표
    z=10, #z 좌표

    vx=-0.347, #x 방향 속도
    vy=0.432, #y 방향 속도
    vz=-0.434, #z 방향 속도

    mass=10000*100, #질량

    color=(255, 120, 120)

)

create_body(

    x=263, #x 좌표
    y=120, #y 좌표
    z=30, #z 좌표

    vx=-0.347, #x 방향 속도
    vy=0.1532, #y 방향 속도
    vz=0.623,

    mass=10000*100, #질량

    color=(120, 180, 255)

)

create_body(

    x=210, #x 좌표
    y=30, #y 좌표
    z=0.1, #z 좌표

    vx=0.694, #x 방향 속도
    vy=-1.364, #y 방향 속도
    vz=-0.123, #z 방향 속도

    mass=10000*100, #질량

    color=(255, 255, 120)

)


# 메인 루프
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        
        # 키 입력
        if event.type == pygame.KEYDOWN:

            # 좌표축
            if event.key == pygame.K_BACKQUOTE:
                show_axis = not show_axis

            # 생성창
            if event.key == pygame.K_TAB:
                show_creator = not show_creator

            # 마지막 물체 삭제
            if event.key == pygame.K_DELETE:

                if len(bodies) > 0:
                    bodies.pop()

            # 시간 가속
            if event.key == pygame.K_EQUALS:
                physics.TIME_SCALE *= 2

            # 시간 감속
            if event.key == pygame.K_MINUS:

                physics.TIME_SCALE /= 2

                if physics.TIME_SCALE < 0.25:
                    physics.TIME_SCALE = 0.25

            
            # 생성 UI 입력
            if show_creator:

                if event.key == pygame.K_UP:

                    selected_field = (
                        selected_field - 1
                    ) % len(fields)

                if event.key == pygame.K_DOWN:

                    selected_field = (
                        selected_field + 1
                    ) % len(fields)

                if event.key == pygame.K_BACKSPACE:

                    key = fields[selected_field]

                    input_values[key] = (
                        input_values[key][:-1]
                    )

                elif event.key == pygame.K_RETURN:

                    try:

                        create_body(

                            x=float(input_values["x"]),
                            y=float(input_values["y"]),
                            z=float(input_values["z"]),

                            vx=float(input_values["vx"]),
                            vy=float(input_values["vy"]),
                            vz=float(input_values["vz"]),

                            mass=float(input_values["mass"]),

                            color=(

                                int(input_values["r"]),
                                int(input_values["g"]),
                                int(input_values["b"])

                            )
                        )

                    except:
                        pass

                else:

                    if event.unicode in "0123456789.-":

                        key = fields[selected_field]

                        input_values[key] += (
                            event.unicode
                        )

        
        # 마우스
        if event.type == pygame.MOUSEBUTTONDOWN:

            camera.handle_mouse_down(
                event.button,
                event.pos
            )

        if event.type == pygame.MOUSEBUTTONUP:

            camera.handle_mouse_up(
                event.button
            )

        if event.type == pygame.MOUSEMOTION:

            camera.handle_mouse_motion(
                event.pos
            )

    
    # 카메라 이동
    keys = pygame.key.get_pressed()

    speed = 8

    forward_x = math.sin(camera.yaw)
    forward_z = math.cos(camera.yaw)

    right_x = math.cos(camera.yaw)
    right_z = -math.sin(camera.yaw)

    if keys[pygame.K_w]:

        camera.x += forward_x * speed
        camera.z += forward_z * speed

    if keys[pygame.K_s]:

        camera.x -= forward_x * speed
        camera.z -= forward_z * speed

    if keys[pygame.K_a]:

        camera.x -= right_x * speed
        camera.z -= right_z * speed

    if keys[pygame.K_d]:

        camera.x += right_x * speed
        camera.z += right_z * speed

    if keys[pygame.K_q]:
        camera.y -= speed

    if keys[pygame.K_e]:
        camera.y += speed

    
    # 물리
    update_physics(bodies)

    
    # 렌더링
    screen.fill((0, 0, 0))

    if show_axis:
        draw_axis(screen, camera)

    draw_bodies(
        screen,
        bodies,
        camera
    )

    
    # UI
    font = pygame.font.SysFont(
        None,
        24
    )

    text = font.render(

        f"Bodies: {len(bodies)}   TimeScale: x{physics.TIME_SCALE:.2f}",

        True,

        (255, 255, 255)

    )

    screen.blit(
        text,
        (10, 10)
    )

    
    # 생성창
    if show_creator:

        pygame.draw.rect(

            screen,
            (30, 30, 30),
            (20, 50, 320, 360)

        )

        title = font.render(

            "CREATE BODY",

            True,

            (255, 255, 255)

        )

        screen.blit(
            title,
            (30, 60)
        )

        for i, field in enumerate(fields):

            color = (

                (255, 255, 0)
                if i == selected_field
                else (255, 255, 255)

            )

            label = font.render(

                f"{field}: {input_values[field]}",

                True,

                color

            )

            screen.blit(
                label,
                (30, 100 + i * 25)
            )

        help_text = font.render(

            "ENTER=create  DELETE=remove",

            True,

            (180, 180, 180)

        )

        screen.blit(
            help_text,
            (30, 335)
        )

    pygame.display.flip()

pygame.quit()