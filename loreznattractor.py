from manim import *

class LorenzAttractor(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-30, 30, 10],
            y_range=[-30, 30, 10],
            z_range=[0, 50, 10],  
            x_length=6,
            y_length=6,
            z_length=3,          
            axis_config={"color": GRAY_C}
        )
        
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, distance=8)
        
        self.play(Create(axes.x_axis), run_time=1)
        self.play(Create(axes.y_axis), run_time=1)
        self.play(Create(axes.z_axis), run_time=1)
        self.wait(0.5)

        
        dt = 0.01
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
        state = np.array([0.1, 0.0, 0.0])
        
        points = []
        for _ in range(2500):
            x, y, z = state
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            
            state += np.array([dx, dy, dz]) * dt
            points.append(axes.coords_to_point(x, y, z))

        path = VMobject(stroke_width=2.5)
        path.set_points_as_corners(points)
        path.set_color(color=[TEAL, PURPLE_A, PINK])

        
        self.begin_ambient_camera_rotation(rate=0.08)
        self.play(Create(path), run_time=12, rate_func=linear)
        self.wait(2)
