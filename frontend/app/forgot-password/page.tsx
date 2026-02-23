'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Mail, Check, X, ArrowLeft } from 'lucide-react';

type ValidationErrors = {
  email?: string;
};

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');
  const [errors, setErrors] = useState<ValidationErrors>({});

  const validateEmail = (value: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!value) {
      return 'Email is required';
    }
    if (!emailRegex.test(value)) {
      return 'Please enter a valid email address';
    }
    return '';
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);
    const emailError = validateEmail(value);
    setErrors({
      ...errors,
      email: emailError,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate
    const emailError = validateEmail(email);
    if (emailError) {
      setErrors({ email: emailError });
      return;
    }

    setIsLoading(true);

    try {
      const API_URL =
        process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      
      const response = await fetch(
        `${API_URL}/auth/forgot-password`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email }),
        }
      );

      if (!response.ok) {
        let error_message = 'Failed to send reset link';
        try {
          const data = await response.json();
          error_message = data.detail || data.message || error_message;
        } catch (e) {
          error_message = `Error ${response.status}: ${response.statusText}`;
        }
        throw new Error(error_message);
      }

      setSubmitted(true);
    } catch (err: any) {
      setError(err.message || 'Failed to send reset link. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const isFormValid = email && !errors.email;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-neutral-900 flex items-center justify-center px-4 py-12">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"></div>
      </div>

      {/* Content */}
      <div className="relative w-full max-w-md">
        {/* Back Button */}
        <Link
          href="/login"
          className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-300 mb-6 transition"
        >
          <ArrowLeft size={16} />
          Back to login
        </Link>

        {/* Card */}
        <div className="bg-slate-900/50 backdrop-blur border border-slate-700/50 rounded-2xl p-8 shadow-2xl">
          {submitted ? (
            // Success State
            <>
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="bg-green-500/20 p-4 rounded-full">
                    <Check className="text-green-400" size={32} />
                  </div>
                </div>
                <h1 className="text-2xl font-bold text-white mb-2">
                  Check Your Email
                </h1>
                <p className="text-gray-400 text-sm mb-6">
                  We've sent a password reset link to <span className="font-semibold text-gray-300">{email}</span>
                </p>
                <p className="text-gray-500 text-xs mb-8">
                  The link will expire in 24 hours. If you don't see the email, check your spam folder.
                </p>
              </div>

              <Link
                href="/login"
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold py-3 rounded-lg hover:from-blue-700 hover:to-blue-800 transition block text-center"
              >
                Back to Login
              </Link>
            </>
          ) : (
            // Form State
            <>
              <div className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">
                  Reset Password
                </h1>
                <p className="text-gray-400 text-sm">
                  Enter your email address and we'll send you a link to reset your password.
                </p>
              </div>

              {error && (
                <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex gap-3">
                  <X className="text-red-400 flex-shrink-0" size={20} />
                  <div>
                    <p className="text-sm font-semibold text-red-400">Error</p>
                    <p className="text-xs text-red-300 mt-1">{error}</p>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Email Input */}
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-semibold text-gray-300 mb-2"
                  >
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3.5 text-gray-500" size={18} />
                    <input
                      id="email"
                      name="email"
                      type="email"
                      required
                      value={email}
                      onChange={handleEmailChange}
                      className={`w-full pl-10 pr-10 py-3 bg-slate-900 border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:border-transparent transition ${
                        errors.email
                          ? 'border-red-500 focus:ring-red-500'
                          : email && !errors.email
                          ? 'border-green-500 focus:ring-green-500'
                          : 'border-slate-600 focus:ring-blue-500'
                      }`}
                      placeholder="you@example.com"
                    />
                    {email && !errors.email && (
                      <Check className="absolute right-3 top-3.5 text-green-400" size={18} />
                    )}
                    {errors.email && (
                      <X className="absolute right-3 top-3.5 text-red-400" size={18} />
                    )}
                  </div>
                  {errors.email && (
                    <p className="mt-1 text-xs text-red-400 flex items-center gap-1">
                      <X size={14} /> {errors.email}
                    </p>
                  )}
                  {email && !errors.email && (
                    <p className="mt-1 text-xs text-green-400 flex items-center gap-1">
                      <Check size={14} /> Email is valid
                    </p>
                  )}
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isLoading || !isFormValid}
                  className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold py-3 rounded-lg hover:from-blue-700 hover:to-blue-800 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed transition"
                >
                  {isLoading ? (
                    <span className="flex items-center justify-center gap-2">
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      Sending...
                    </span>
                  ) : (
                    'Send Reset Link'
                  )}
                </button>

                {/* Divider */}
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-slate-600"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-slate-900/50 text-gray-400">or</span>
                  </div>
                </div>

                {/* Back to Login Link */}
                <Link
                  href="/login"
                  className="w-full border border-slate-600 text-gray-300 font-semibold py-3 rounded-lg hover:border-slate-500 hover:bg-slate-900/50 transition text-center block"
                >
                  Back to Login
                </Link>
              </form>
            </>
          )}

          {/* Help Section */}
          <div className="mt-8 pt-6 border-t border-slate-700">
            <p className="text-xs text-gray-500 text-center">
              <span className="font-semibold">Need help?</span> If you don't receive the reset link within a few minutes, check your spam folder or{' '}
              <Link href="/" className="text-blue-400 hover:text-blue-300">
                contact support
              </Link>
              .
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
