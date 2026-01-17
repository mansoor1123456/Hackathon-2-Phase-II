import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Protected routes
  const protectedPaths = ['/dashboard', '/profile'];
  const isProtectedPath = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // ✅ Only read token from cookies (server-side)
  const token = request.cookies.get('todo_app_token')?.value;

  // Redirect if accessing protected route without token
  if (isProtectedPath && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Allow access
  return NextResponse.next();
}

// Paths to apply middleware
export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
