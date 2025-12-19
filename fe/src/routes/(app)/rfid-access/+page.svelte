<script lang="ts">
	import { onMount } from 'svelte';
	import { ref, onValue } from 'firebase/database';
	import { db } from '$lib/firebase';
	import Breadcrumb from '../../../components/breadcrumb/Breadcrumb.svelte';
	import { Radio, Search, ChevronDown, Filter } from 'lucide-svelte';

	interface RfidLog {
		id: string;
		rfidId: string;
		date: string;
		time: string;
		rssi: number;
		tag: string;
		timestamp: number; // for sorting
	}

	let logs: RfidLog[] = [];
	let loading = true;

	// Filter states
	let searchQuery = '';
	let selectedRfidSource = '';
	let selectedTag = '';

	// Derived values for dropdown options
	$: uniqueRfidSources = [...new Set(logs.map((log) => log.rfidId).filter(Boolean))].sort();
    $: uniqueTags = [...new Set(logs.map((log) => log.tag).filter(Boolean))].sort();

    // Filter logic
    $: filteredLogs = logs.filter((log) => {
        const searchLower = searchQuery.toLowerCase();
        
        // Helper function untuk cek data dengan aman (mencegah error jika data kosong/undefined)
        const safeIncludes = (val: any) => 
            String(val || '').toLowerCase().includes(searchLower);

        const matchesSearch =
            searchQuery.length < 3 ||
            safeIncludes(log.tag) ||
            safeIncludes(log.rfidId) ||
            safeIncludes(log.date) ||
            safeIncludes(log.time) ||
            safeIncludes(log.rssi);

        const matchesRfid = selectedRfidSource === '' || log.rfidId === selectedRfidSource;
        const matchesTag = selectedTag === '' || log.tag === selectedTag;

        return matchesSearch && matchesRfid && matchesTag;
    });

	onMount(() => {
		const rfidRef = ref(db, '/');
		
		const unsubscribe = onValue(rfidRef, (snapshot) => {
			const data = snapshot.val();
			const newLogs: RfidLog[] = [];

			if (data) {
				// Iterate through RFID devices (rfidA, rfidB, etc.)
				Object.keys(data).forEach((rfidId) => {
					const rfidData = data[rfidId];
					if (rfidData && rfidData.history) {
						// Iterate through dates
						Object.keys(rfidData.history).forEach((date) => {
							const dateData = rfidData.history[date];
							// Iterate through times
							Object.keys(dateData).forEach((time) => {
								const entry = dateData[time];
								newLogs.push({
									id: `${rfidId}-${date}-${time}`,
									rfidId: rfidId,
									date: date,
									time: time,
									rssi: entry.rssi,
									tag: entry.tag,
									timestamp: new Date(`${date}T${time.replace(/:/g, ':').replace(/(\d{2}:\d{2}:\d{2}):(\d{3})/, '$1.$2')}`).getTime()
								});
							});
						});
					}
				});
			}

			// Sort by timestamp descending (newest first)
			logs = newLogs.sort((a, b) => b.timestamp - a.timestamp);
			loading = false;
		});

		return () => unsubscribe();
	});
</script>

<div class="flex flex-col gap-y-6">
	<Breadcrumb pageName="RFID Access Logs" />

	<!-- Search and Filter Controls -->
	<div class="flex flex-col gap-4 rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03] md:flex-row md:items-center md:justify-between">
		<div class="relative w-full md:w-72">
			<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
				<Search class="h-5 w-5 text-gray-400" />
			</div>
			<input
				type="text"
				bind:value={searchQuery}
				class="block w-full rounded-lg border border-gray-200 bg-transparent py-2.5 pl-10 pr-4 text-sm text-gray-900 placeholder-gray-400 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:text-white dark:focus:border-brand-500 dark:focus:ring-brand-500"
				placeholder="Search by tag, source, or date..."
			/>
		</div>

		<div class="flex flex-col gap-3 sm:flex-row sm:items-center">
			<div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 sm:hidden">
				<Filter class="h-4 w-4" />
				<span>Filters:</span>
			</div>
			
			<div class="relative w-full sm:w-48">
				<select
					bind:value={selectedRfidSource}
					class="block w-full appearance-none rounded-lg border border-gray-200 bg-transparent py-2.5 pl-4 pr-10 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:text-white dark:focus:border-brand-500 dark:focus:ring-brand-500"
				>
					<option value="">All Sources</option>
					{#each uniqueRfidSources as source}
						<option value={source}>{source}</option>
					{/each}
				</select>
				<div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
					<ChevronDown class="h-4 w-4 text-gray-500" />
				</div>
			</div>

			<div class="relative w-full sm:w-48">
				<select
					bind:value={selectedTag}
					class="block w-full appearance-none rounded-lg border border-gray-200 bg-transparent py-2.5 pl-4 pr-10 text-sm text-gray-900 focus:border-brand-500 focus:ring-brand-500 dark:border-gray-700 dark:text-white dark:focus:border-brand-500 dark:focus:ring-brand-500"
				>
					<option value="">All Tags</option>
					{#each uniqueTags as tag}
						<option value={tag}>{tag}</option>
					{/each}
				</select>
				<div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
					<ChevronDown class="h-4 w-4 text-gray-500" />
				</div>
			</div>
		</div>
	</div>

	<div class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
		<div class="max-w-full overflow-x-auto">
			<table class="min-w-full bg-transparent text-left text-sm text-gray-900 dark:text-gray-100">
				<thead class="bg-gray-50 dark:bg-white/[0.03]">
					<tr>
						<th class="px-5 py-3 font-medium text-gray-500 dark:text-gray-400">Date Time</th>
						<th class="px-5 py-3 font-medium text-gray-500 dark:text-gray-400">RFID Source</th>
						<th class="px-5 py-3 font-medium text-gray-500 dark:text-gray-400">Tag</th>
						<th class="px-5 py-3 font-medium text-gray-500 dark:text-gray-400">RSSI</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-gray-800">
					{#if loading}
						<tr>
							<td colspan="4" class="px-5 py-4 text-center text-gray-500">Loading data...</td>
						</tr>
					{:else if logs.length === 0}
						<tr>
							<td colspan="4" class="px-5 py-4 text-center text-gray-500">No logs found</td>
						</tr>
					{:else if filteredLogs.length === 0}
						<tr>
							<td colspan="4" class="px-5 py-4 text-center text-gray-500">No matching logs found</td>
						</tr>
					{:else}
						{#each filteredLogs as log (log.id)}
							<tr class="hover:bg-gray-50 dark:hover:bg-white/[0.03]">
								<td class="px-5 py-4 whitespace-nowrap">
									<div class="flex flex-col">
										<span class="font-medium">{log.date}</span>
										<span class="text-xs text-gray-500">{log.time}</span>
									</div>
								</td>
								<td class="px-5 py-4">
									<div class="flex items-center gap-2">
										<div class="flex h-8 w-8 items-center justify-center rounded-full bg-brand-50 text-brand-500 dark:bg-brand-500/10 dark:text-brand-400">
											<Radio class="h-4 w-4" />
										</div>
										<span class="font-medium">{log.rfidId}</span>
									</div>
								</td>
								<td class="px-5 py-4">
									<span class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10 dark:bg-blue-400/10 dark:text-blue-400 dark:ring-blue-400/30">
										{log.tag}
									</span>
								</td>
								<td class="px-5 py-4 font-mono text-gray-600 dark:text-gray-400">
									{log.rssi}
								</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
		</div>
	</div>
</div>