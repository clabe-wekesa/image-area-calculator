import cv2


def select_two_points(img, window_name="img"):
    """
    Scrollbar-based viewer for selecting exactly two points.
    Uses OpenCV trackbars as scrollbars (no zoom).

    Controls:
      Mouse click : select points (max 2)
      Scrollbars : move around image
      ENTER      : confirm after 2 points
      ESC        : abort

    Returns:
      [(x1, y1), (x2, y2)] in ORIGINAL image coordinates
    """

    h, w = img.shape[:2]

    # Viewport size (what you see at once)
    view_w = min(1200, w)
    view_h = min(800, h)

    # Scroll positions
    x0, y0 = 0, 0

    points = []

    def clamp(v, lo, hi):
        return max(lo, min(v, hi))

    # ----------------------------
    # Mouse callback
    # ----------------------------
    def mouse_cb(event, x, y, flags, param):
        nonlocal points, y0

        # --- Mouse wheel = vertical scroll ---
        if event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                y0 = clamp(y0 - 60, 0, h - view_h)  # scroll up
            else:
                y0 = clamp(y0 + 60, 0, h - view_h)  # scroll down

            # keep Y trackbar synced
            cv2.setTrackbarPos("Y", window_name, y0)
            return

        # --- Left click = select point ---
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
            ox = x0 + x
            oy = y0 + y
            if 0 <= ox < w and 0 <= oy < h:
                points.append((ox, oy))

    # ----------------------------
    # Window + trackbars
    # ----------------------------
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    def on_x(val):
        nonlocal x0
        x0 = clamp(val, 0, w - view_w)

    def on_y(val):
        nonlocal y0
        y0 = clamp(val, 0, h - view_h)

    cv2.createTrackbar("Horizontal (X)", window_name, 0, max(0, w - view_w), on_x)
    cv2.createTrackbar("Vertical (Y)", window_name, 0, max(0, h - view_h), on_y)

    cv2.setMouseCallback(window_name, mouse_cb)

    # ----------------------------
    # Main loop
    # ----------------------------
    while True:
        view = img[y0:y0 + view_h, x0:x0 + view_w].copy()

        # Draw points
        for px, py in points:
            vx, vy = px - x0, py - y0
            if 0 <= vx < view_w and 0 <= vy < view_h:
                cv2.circle(view, (vx, vy), 4, (0, 0, 255), -1)

        # Draw line
        if len(points) == 2:
            p1, p2 = points
            v1 = (p1[0] - x0, p1[1] - y0)
            v2 = (p2[0] - x0, p2[1] - y0)
            if all(0 <= v < view_w for v in (v1[0], v2[0])) and \
               all(0 <= v < view_h for v in (v1[1], v2[1])):
                cv2.line(view, v1, v2, (0, 0, 255), 2)

        cv2.imshow(window_name, view)
        key = cv2.waitKey(30) & 0xFF

        if len(points) == 2 and key in (13, 10):  # ENTER
            break
        if key == 27:  # ESC
            break

    cv2.destroyWindow(window_name)
    return points
