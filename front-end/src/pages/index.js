import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../context/AuthContext';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      router.replace('/tasks');
    } else {
      router.replace('/login');
    }
  }, [isAuthenticated, router]);

  // Return null since this is just a redirect page
  return null;
}
