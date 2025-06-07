<script lang="ts">
	import '../styles/app.css';
	import { Toaster } from 'svelte-french-toast';
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';

	let { children } = $props();
	const queryClient = new QueryClient();
</script>

<QueryClientProvider client={queryClient}>
	<Toaster />
	{@render children()}
</QueryClientProvider>
