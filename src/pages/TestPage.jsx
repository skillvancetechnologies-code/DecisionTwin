import React, { useState } from "react";

function TestPage() {
  const [count, setCount] = useState(0);

  return (
    <div className="p-10">
      <h1>Test Page</h1>

      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
    </div>
  );
}

export default TestPage;