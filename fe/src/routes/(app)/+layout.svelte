<script lang="ts">
	import { Toaster } from 'svelte-french-toast';
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
	import Header from '../../components/header/Header.svelte';
	import Sidebar from '../../components/sidebar/Sidebar.svelte';
	import HasAuth from '../../viewports/HasAuth.svelte';

	let { children } = $props();

	let sidebarToggle = $state(false);
	let menuToggle = $state(false);

	const queryClient = new QueryClient();
</script>

<QueryClientProvider client={queryClient}>
	<Toaster />
	<HasAuth>
		<div class="flex h-screen overflow-hidden">
			<Sidebar bind:sidebarToggle />
			<div class="relative flex flex-1 flex-col overflow-x-hidden overflow-y-auto">
				<Header bind:sidebarToggle bind:menuToggle />

				<main>
					<div class="mx-auto max-w-(--breakpoint-2xl) p-4 md:p-6">
						{@render children()}
					</div>
				</main>
			</div>
		</div>
	</HasAuth>
</QueryClientProvider>
