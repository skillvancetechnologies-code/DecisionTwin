import { Component } from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center">
          <h1 className="text-2xl font-bold text-risk-high">Something went wrong</h1>
          <p className="max-w-md text-gray-600">{this.state.error.message}</p>
          <button className="btn-primary" onClick={() => window.location.assign("/")}>
            Back home
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
