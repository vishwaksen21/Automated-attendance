"use client";

import React, { useState, useCallback } from "react";
import { AlertCircle, CheckCircle, Info, X } from "lucide-react";

interface ToastMessage {
  id: string;
  message: string;
  type: "success" | "error" | "warning" | "info";
  duration?: number;
}

interface ToastProviderProps {
  children: React.ReactNode;
}

interface ToastContextType {
  showToast: (
    message: string,
    type: "success" | "error" | "warning" | "info",
    duration?: number
  ) => void;
  removeToast: (id: string) => void;
}

const ToastContext = React.createContext<ToastContextType | undefined>(
  undefined
);

export function ToastProvider({ children }: ToastProviderProps) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const showToast = useCallback(
    (
      message: string,
      type: "success" | "error" | "warning" | "info",
      duration = 3000
    ) => {
      const id = Math.random().toString(36).substr(2, 9);
      const newToast: ToastMessage = { id, message, type, duration };

      setToasts((prev: ToastMessage[]) => [...prev, newToast]);

      if (duration > 0) {
        setTimeout(() => removeToast(id), duration);
      }
    },
    []
  );

  const removeToast = useCallback((id: string) => {
    setToasts((prev: ToastMessage[]) => prev.filter((toast: ToastMessage) => toast.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ showToast, removeToast }}>
      {children}
      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within ToastProvider");
  }
  return context;
}

interface ToastContainerProps {
  toasts: ToastMessage[];
  onRemove: (id: string) => void;
}

function ToastContainer({ toasts, onRemove }: ToastContainerProps) {
  const bgColors = {
    success: "bg-green-500",
    error: "bg-red-500",
    warning: "bg-yellow-500",
    info: "bg-blue-500",
  };

  const icons = {
    success: <CheckCircle className="w-5 h-5" />,
    error: <AlertCircle className="w-5 h-5" />,
    warning: <AlertCircle className="w-5 h-5" />,
    info: <Info className="w-5 h-5" />,
  };

  return (
    <div className="fixed top-4 right-4 space-y-2 z-50">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`${bgColors[toast.type]} text-white px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 animate-in fade-in slide-in-from-right duration-300`}
        >
          {icons[toast.type]}
          <span className="flex-1 font-medium">{toast.message}</span>
          <button
            onClick={() => onRemove(toast.id)}
            className="hover:opacity-80 transition-opacity"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      ))}
    </div>
  );
}

// Example usage component
export function ToastExample() {
  const { showToast } = useToast();

  return (
    <div className="space-y-4">
      <button
        onClick={() => showToast("Operation successful!", "success")}
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Success
      </button>
      <button
        onClick={() => showToast("Something went wrong!", "error")}
        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Error
      </button>
      <button
        onClick={() => showToast("Please check your input", "warning")}
        className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
      >
        Warning
      </button>
      <button
        onClick={() => showToast("Information for you", "info")}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Info
      </button>
    </div>
  );
}
