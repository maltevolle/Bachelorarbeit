from pxr import UsdGeom, Gf
import omni.usd
import omni.kit.app
import time

stage = omni.usd.get_context().get_stage()
prim_path = "/World/TCP"
prim = stage.GetPrimAtPath(prim_path)

def load_waypoints():
    convpoints = []
    with open("C:/Users/volle/Documents/output.txt", "r") as f:
        for line in f:
            if line.strip():
                x, y, z = map(float, line.strip().split())
                convpoints.append(Gf.Vec3d(x, y, z))
    return convpoints

if not prim.IsValid():
    print(f"[ERROR] Prim not found at {prim_path}")
else:
    xform = UsdGeom.Xformable(prim)
    xform_ops = xform.GetOrderedXformOps()
    translate_op = next((op for op in xform_ops if op.GetOpType() == UsdGeom.XformOp.TypeTranslate), None)

    if translate_op is None:
        print("[WARN] No translateOp found.")
    else:
        waypoints = load_waypoints()
        if not waypoints:
            print("[ERROR] No waypoints loaded.")
        else:
            update_stream = omni.kit.app.get_app().get_update_event_stream()

            current_segment = [0]  # List for mutable reference
            segment_start_time = [time.time()]
            segment_duration = 2.0  # Sekunden pro Wegpunkt-Übergang

            def on_update(event):
                now = time.time()
                idx = current_segment[0]

                if idx >= len(waypoints) - 1:
                    print("[INFO] Animation complete.")
                    update_stream.unsubscribe(on_update_sub)
                    return

                start = waypoints[idx]
                end = waypoints[idx + 1]
                t = (now - segment_start_time[0]) / segment_duration
                t = min(t, 1.0)
                new_pos = start * (1 - t) + end * t
                translate_op.Set(new_pos)

                if t >= 1.0:
                    current_segment[0] += 1
                    segment_start_time[0] = now

            on_update_sub = update_stream.create_subscription_to_pop(on_update)
