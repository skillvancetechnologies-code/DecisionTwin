import { useCallback } from "react";
import { useDropzone } from "react-dropzone";

export default function UploadDropzone({ file, onFile }) {
  const onDrop = useCallback(
    (accepted) => {
      if (accepted?.[0]) onFile(accepted[0]);
    },
    [onFile]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "text/csv": [".csv"] },
    maxFiles: 1,
  });

  return (
    <div
      {...getRootProps()}
      className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-10 text-center transition ${
        isDragActive
          ? "border-brand-orange bg-brand-orange/5"
          : "border-surface-border bg-white hover:border-brand-teal"
      }`}
    >
      <input {...getInputProps()} aria-label="CSV file upload" />
      {file ? (
        <div>
          <p className="font-medium text-brand-navy">{file.name}</p>
          <p className="text-sm text-gray-500">
            {(file.size / 1024).toFixed(1)} KB · click to replace
          </p>
        </div>
      ) : (
        <div>
          <p className="font-medium text-brand-navy">
            Drag & drop a CSV here, or click to browse
          </p>
          <p className="text-sm text-gray-500">Sales, HR, or marketing data</p>
        </div>
      )}
    </div>
  );
}
