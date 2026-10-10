import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "NewsScope — News Article Classifier";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "80px",
          backgroundColor: "#f7f6f3",
          fontFamily: "sans-serif",
        }}
      >
        {/* Top bar */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <div
              style={{
                width: "48px",
                height: "48px",
                borderRadius: "12px",
                backgroundColor: "#0f0f0e",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#ffffff",
                fontSize: "24px",
                fontWeight: "bold",
              }}
            >
              N
            </div>
            <span style={{ fontSize: "28px", fontWeight: "700", color: "#0f0f0e", letterSpacing: "-0.5px" }}>
              NewsScope
            </span>
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              padding: "8px 18px",
              borderRadius: "9999px",
              backgroundColor: "#f1efeb",
              border: "1px solid #e7e3dd",
              fontSize: "16px",
              fontWeight: "600",
              color: "#4f46e5",
            }}
          >
            BBC News 5-Class Benchmark
          </div>
        </div>

        {/* Center content */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <h1
            style={{
              fontSize: "56px",
              fontWeight: "800",
              color: "#0f0f0e",
              lineHeight: 1.1,
              letterSpacing: "-1.5px",
              margin: 0,
            }}
          >
            News Article Classifier
          </h1>
          <p
            style={{
              fontSize: "24px",
              color: "#57534e",
              lineHeight: 1.4,
              margin: 0,
              maxWidth: "900px",
            }}
          >
            AI-powered news classification across 5 domains with sub-millisecond inference and transparent confidence distributions.
          </p>
        </div>

        {/* Bottom category pills */}
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          {["Business", "Entertainment", "Politics", "Sport", "Tech"].map((cat) => (
            <div
              key={cat}
              style={{
                padding: "8px 20px",
                borderRadius: "9999px",
                backgroundColor: "#ffffff",
                border: "1px solid #e7e3dd",
                fontSize: "16px",
                fontWeight: "600",
                color: "#3f3d3a",
              }}
            >
              {cat}
            </div>
          ))}
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
