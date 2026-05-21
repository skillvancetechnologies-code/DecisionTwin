// Week 2 completedgit status
import { useDropzone } from "react-dropzone";
import React, { useState } from "react";
import { Link } from "react-router-dom";

function UploadPage() {

  const [file, setFile] = useState(null);
  const [previewData, setPreviewData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fileType, setFileType] =
  useState("sales");

  const { getRootProps, getInputProps } =
useDropzone({

 accept: {
  
},


  onDrop: async (acceptedFiles) => {

    const selectedFile =
      acceptedFiles[0];

    if (!selectedFile) return;

setError("");

if (!selectedFile.name.endsWith(".csv")) {

  setError(
    "Only CSV files are allowed"
  );

  return;
}

if (selectedFile.size === 0) {

  setError(
    "Uploaded file is empty"
  );

  return;
}

setFile(selectedFile);
setLoading(true);

try {

  const formData =
    new FormData();

  formData.append(
    "file",
    selectedFile
  );

  const response =
    await fetch(
      "http://127.0.0.1:8000/upload/",
      {
        method: "POST",
        body: formData
      }
    );

  console.log(response);

const result =
  await response.json();

console.log(
  "Backend response:",
  result
);

setPreviewData([

  {
    id: "Uploaded",
    revenue: result?.filename || "No filename",
    month: result?.content_type || "Unknown"
  }

]);

setError("");

}

catch(error) {

  console.log(
    "Actual error:",
    error
  );

  setError(
    error.message
  );

}

setLoading(false);


  }

});

  return (

    <div className="min-h-screen bg-[#050816] p-10 text-white">

      <div className="flex items-center justify-between mb-8">

  <h1 className="text-5xl font-bold">
    Upload Dataset
  </h1>

  <Link
    to="/dashboard"
    className="rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 px-6 py-3"
  >
    Back to Dashboard
  </Link>

</div>
      <div className="rounded-3xl border-2 border-dashed border-purple-500 p-10 text-center">

       <div
  {...getRootProps()}
  className="cursor-pointer rounded-xl bg-purple-600 px-6 py-6"
>

  <input {...getInputProps()} />

  <p>
    Drag CSV here or click to upload
  </p>

</div>

       
<p className="mt-6">

  {loading
    ? "⏳ Processing dataset..."
    : file
      ? `Selected file: ${file.name}`
      : "No file selected"}

</p>

{error && (

  <div className="mt-4 rounded-xl bg-red-500/20 border border-red-500 p-3 text-red-300">

    {error}

  </div>

)}
        <div className="mt-6">

  <label className="block mb-2">
    Dataset Type
  </label>

 <select
  value={fileType}
  onChange={(e) =>
    setFileType(e.target.value)
  }
  className="rounded-xl bg-[#1a1a2e] border border-white/10 px-4 py-2 text-white outline-none"
>

  <option value="sales" className="bg-[#1a1a2e] text-white">
    Sales
  </option>

  <option value="hr" className="bg-[#1a1a2e] text-white">
    HR
  </option>

  <option value="marketing" className="bg-[#1a1a2e] text-white">
    Marketing
  </option>

  <option value="customer" className="bg-[#1a1a2e] text-white">
    Customer
  </option>

  <option value="ops" className="bg-[#1a1a2e] text-white">
    Operations
  </option>

  <option value="financial" className="bg-[#1a1a2e] text-white">
    Financial
  </option>

</select>
</div>

      </div>


      {previewData.length > 0 && (

        <div className="mt-10">

          <h2 className="mb-4 text-3xl font-bold">

            Preview

          </h2>

          <table className="w-full rounded-xl overflow-hidden bg-white/5">

            <thead className="bg-purple-700">

              <tr>

                <th className="p-4">
                  ID
                </th>

                <th className="p-4">
                  Revenue
                </th>

                <th className="p-4">
                  Month
                </th>

              </tr>

            </thead>

            <tbody>

              {previewData.map((row, index) => (

                <tr
                  key={index}
                  className="border-b border-white/10 text-center"
                >

                  <td className="p-4">
                    {row.id}
                  </td>

                  <td className="p-4">
                    {row.revenue}
                  </td>

                  <td className="p-4">
                    {row.month}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      )}

    </div>

  );
}

export default UploadPage;