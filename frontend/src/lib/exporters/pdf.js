import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

/** Capture a DOM node (the dashboard) and wrap it in a single-page PDF. */
export async function exportDashboardSnapshot(node, filename = "dashboard.pdf") {
  if (!node) return;
  const canvas = await html2canvas(node, { scale: 2, backgroundColor: "#ffffff" });
  const img = canvas.toDataURL("image/png");
  const pdf = new jsPDF({ orientation: "landscape", unit: "px", format: "a4" });
  const pageW = pdf.internal.pageSize.getWidth();
  const pageH = pdf.internal.pageSize.getHeight();
  const ratio = Math.min(pageW / canvas.width, pageH / canvas.height);
  const w = canvas.width * ratio;
  const h = canvas.height * ratio;
  pdf.addImage(img, "PNG", (pageW - w) / 2, 20, w, h);
  pdf.save(filename);
}
