#for video only
from playwright.sync_api import Page

video = False


def show_overlay(page: Page, test_name: str, status: str):
    if not video:
        return
    color_map = {
        "RUNNING": "#1e90ff",
        "PASS": "#22c55e",
        "FAIL": "#ef4444"
    }
    color = color_map.get(status, "#1e90ff")
    page.evaluate(
        """
        ({testName, status, color}) => {
            const id = "__automation_demo_overlay__";
            const old = document.getElementById(id);
            if (old) old.remove();

            // container
            const wrapper = document.createElement("div");
            wrapper.id = id;

            // badge
            const badge = document.createElement("span");
            badge.textContent = status;
            badge.style.background = color;
            badge.style.color = "#fff";
            badge.style.fontWeight = "600";
            badge.style.fontSize = "12px";
            badge.style.letterSpacing = "0.6px";
            badge.style.padding = "4px 8px";
            badge.style.borderRadius = "6px";
            badge.style.whiteSpace = "nowrap";

            // test name
            const title = document.createElement("span");
            title.textContent = testName;
            title.style.fontWeight = "500";
            title.style.opacity = "0.9";

            wrapper.appendChild(badge);
            wrapper.appendChild(title);

            Object.assign(wrapper.style, {
                position: "fixed",
                top: "16px",
                left: "16px",
                display: "flex",
                gap: "12px",
                alignItems: "center",
                padding: "10px 14px",
                background: "rgba(20, 20, 20, 0.85)",
                color: "#fff",
                borderRadius: "10px",
                fontFamily: "Inter, Arial, sans-serif",
                fontWeight: "bold",
                fontSize: "30px",
                boxShadow: "0 8px 20px rgba(0,0,0,0.25)",
                zIndex: "999999",
                pointerEvents: "none",
                opacity: "0",
                transform: "translateY(-10px)",
                transition: "opacity 0.4s ease, transform 0.4s ease"
            });

            document.body.appendChild(wrapper);

            // animate in
            requestAnimationFrame(() => {
                wrapper.style.opacity = "1";
                wrapper.style.transform = "translateY(0)";
            });

            // animate out
            setTimeout(() => {
                wrapper.style.opacity = "0";
                wrapper.style.transform = "translateY(-10px)";
            }, 3000);

            // cleanup
            setTimeout(() => wrapper.remove(), 2000);
        }
        """,
        {"testName": test_name, "status": status, "color": color}
    )
    page.wait_for_timeout(2000)


click_script = """
            () => {
                document.addEventListener("mousedown", (e) => {
                const ripple = document.createElement("div");
                ripple.style.position = "fixed";
                ripple.style.left = e.clientX + "px";
                  ripple.style.top = e.clientY + "px";
                  ripple.style.width = "30px";
                  ripple.style.height = "30px";
                  ripple.style.border = "2px solid red";
                  ripple.style.borderRadius = "50%";
                  ripple.style.pointerEvents = "none";
                  ripple.style.transform = "translate(-50%, -50%) scale(0)";
                  ripple.style.opacity = "0.8";
                  ripple.style.transition = "transform 0.2s ease-out, opacity 0.3s ease-out";
                  document.body.appendChild(ripple);
                  requestAnimationFrame(() => {
                    ripple.style.transform = "translate(-50%, -50%) scale(2.5)";
                    ripple.style.opacity = "0";
                  });
                  setTimeout(() => ripple.remove(), 700);
                });
            }
        """ if video else ""

fill_script = """
               (el) => {
                   const origShadow = el.style.boxShadow;
                   const origBackground = el.style.backgroundColor;
                   el.style.border = '3px solid red'; 
                   el.style.boxShadow = '0 0 10px 4px rgba(0, 150, 255, 0.7)';
                   el.style.backgroundColor = '#eeebd0';

                   setTimeout(() => {
                       el.style.boxShadow = origShadow;
                       el.style.backgroundColor = origBackground;
                   }, 300);
               }
           """ if video else ""
