import math


# 중력상수 상수
G = 0.0008

# 충돌 방지용 소프트닝 상수
SOFTENING = 25

# 시간 배속
TIME_SCALE = 0.25


def update_physics(bodies):

    dt = 0.5 * TIME_SCALE

    accelerations = []

    
    # 중력 계산
    for i, body1 in enumerate(bodies):

        ax = ay = az = 0.0

        for j, body2 in enumerate(bodies):

            if i == j:
                continue

            dx = body2.x - body1.x
            dy = body2.y - body1.y
            dz = body2.z - body1.z

            # 거리 제곱
            dist_sq = (

                dx * dx +
                dy * dy +
                dz * dz +
                SOFTENING

            )

            dist = math.sqrt(dist_sq)

            # 만유인력 공식
            force = (

                G *
                body1.mass *
                body2.mass /
                dist_sq

            )

            # 가속도
            accel = force / body1.mass

            ax += accel * dx / dist
            ay += accel * dy / dist
            az += accel * dz / dist

        accelerations.append(
            (ax, ay, az)
        )

    
    # 속도 업데이트
    for i, body in enumerate(bodies):

        ax, ay, az = accelerations[i]

        body.vx += ax * dt
        body.vy += ay * dt
        body.vz += az * dt

    
    # 위치 업데이트
    for body in bodies:

        body.x += body.vx * dt
        body.y += body.vy * dt
        body.z += body.vz * dt

        body.update_trail()