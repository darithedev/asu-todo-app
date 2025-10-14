import Head from 'next/head'

export default function Home() {
  return (
    <>
      <Head>
        <title>ASU Todo App</title>
        <meta name="description" content="A simple todo app for managing your tasks" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <h1 className="text-4xl font-bold text-gray-900">Welcome to ASU Todo App</h1>
            <p className="mt-4 text-lg text-gray-500">
              Get started by logging in or creating a new account.
            </p>
          </div>
        </div>
      </main>
    </>
  )
}
