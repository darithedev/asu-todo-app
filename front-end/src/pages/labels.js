import { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useAuth } from '../context/AuthContext';
import { labelService } from '../services/labels';
import LabelList from '../components/LabelList';

export default function Labels() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();
  const [labels, setLabels] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    loadLabels();
  }, [user?.id]);

  const loadLabels = async () => {
    if (!user?.id) return;
    
    try {
      const data = await labelService.getUserLabels(user.id);
      setLabels(data);
    } catch (err) {
      setError('Failed to load labels');
      console.error('Error loading labels:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateLabel = async (labelData) => {
    try {
      setError(''); // Clear any previous errors
      const newLabel = await labelService.createLabel(labelData);
      setLabels([...labels, newLabel]);
    } catch (err) {
      console.error('Error creating label:', err);
      setError(err.message || 'Failed to create label');
      return false; // Return false to indicate failure
    }
    return true; // Return true to indicate success
  };

  const handleUpdateLabel = async (labelId, updates) => {
    try {
      const updatedLabel = await labelService.updateLabel(labelId, updates);
      setLabels(labels.map(label => label.id === labelId ? updatedLabel : label));
    } catch (err) {
      setError(err.message || 'Failed to update label');
    }
  };

  const handleDeleteLabel = async (labelId) => {
    try {
      await labelService.deleteLabel(labelId);
      setLabels(labels.filter(label => label.id !== labelId));
    } catch (err) {
      setError(err.message || 'Failed to delete label');
    }
  };

  return (
    <>
      <Head>
        <title>Manage Labels - ASU Todo App</title>
        <meta name="description" content="Manage your task labels" />
      </Head>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Manage Labels
            </h2>
          </div>
        </div>

        {error && (
          <div className="rounded-md bg-red-50 p-4 mt-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">{error}</h3>
              </div>
            </div>
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-8">
            <div className="inline-flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading labels...
            </div>
          </div>
        ) : (
          <div className="mt-6">
            <LabelList
              labels={labels}
              onCreateLabel={handleCreateLabel}
              onUpdateLabel={handleUpdateLabel}
              onDeleteLabel={handleDeleteLabel}
            />
          </div>
        )}
      </div>
    </>
  );
}
