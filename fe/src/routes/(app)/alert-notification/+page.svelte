<script lang="ts">
	import {
		Check,
		ChevronDown,
		ChevronLeft,
		ChevronRight,
		Clock,
		Download,
		Filter,
		MapPin,
		Maximize,
		RefreshCcw,
		Save
	} from '@lucide/svelte';
	import Breadcrumb from '../../../components/breadcrumb/Breadcrumb.svelte';
	import { liveAlertDummy, monitoringDummy } from '../live-monitoring/data';
	import { slide } from 'svelte/transition';

	let checkboxToggle = $state(false);
	let openAlertFilters = $state(false);
</script>

<div class="flex flex-col gap-y-6">
	<Breadcrumb pageName="Alert & Notification" />
	<!-- Alert History -->
	<div
		class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
	>
		<div
			class="flex flex-col gap-y-2 border-b border-gray-100 px-6 py-4 md:flex-row md:items-center md:justify-between dark:border-gray-800"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Alert History</h3>
			<div class="flex items-center gap-x-2">
				<button aria-label="exportButton" class="btn-primary-sm">
					<Download class="h-4 w-4" />
					Export
				</button>
				<button aria-label="exportButton" class="btn-primary-sm">
					<RefreshCcw class="h-4 w-4" />
					Refresh
				</button>
				<div class="relative inline-block">
					<button
						onclick={() => (openAlertFilters = !openAlertFilters)}
						aria-label="exportButton"
						class="btn-primary-outline-sm"
					>
						<Filter class="h-4 w-4" />
						Filters
					</button>
					{#if openAlertFilters}
						<div class="dropdown" transition:slide>
							<ul class="flex flex-col gap-y-2">
								<!-- Alert Types -->
								<li class="form-groups">
									<span class="form-label">Alert Type</span>
									<div class="relative z-20 bg-transparent">
										<select class="select-input">
											<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>Select option</option
											>
											{#each ['Motion Detection', 'Intrusion', 'Face Recognition', 'Unattended Object'] as option}
												<option
													value={option}
													class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>
													{option}
												</option>
											{/each}
										</select>
										<span
											class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
										>
											<ChevronDown class="h-5 w-5" />
										</span>
									</div>
								</li>
								<!-- Location -->
								<li class="form-groups">
									<span class="form-label">Location</span>
									<div class="relative z-20 bg-transparent">
										<select class="select-input">
											<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>Select option</option
											>
											{#each monitoringDummy as option}
												<option
													value={option.name}
													class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>
													{option.name}
												</option>
											{/each}
										</select>
										<span
											class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
										>
											<ChevronDown class="h-5 w-5" />
										</span>
									</div>
								</li>
								<!-- Status -->
								<li class="form-groups">
									<span class="form-label">Status</span>
									<div class="relative z-20 bg-transparent">
										<select class="select-input">
											<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>Select option</option
											>
											{#each ['Pending', 'Acknowledged', 'Resolved'] as option}
												<option
													value={option}
													class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>
													{option}
												</option>
											{/each}
										</select>
										<span
											class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
										>
											<ChevronDown class="h-5 w-5" />
										</span>
									</div>
								</li>
								<!-- Date Range -->
								<li class="form-groups">
									<span class="form-label">Date Range</span>
									<div class="relative z-20 bg-transparent">
										<select class="select-input">
											<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>Select option</option
											>
											{#each ['Yesterday', 'Last 7 Days', 'Last 30 Days'] as option}
												<option
													value={option}
													class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>
													{option}
												</option>
											{/each}
										</select>
										<span
											class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
										>
											<ChevronDown class="h-5 w-5" />
										</span>
									</div>
								</li>
								<!-- Apply Button -->
								<li class="mt-4 flex flex-col justify-end lg:flex-row">
									<button class="btn-primary-md">
										<Filter class="h-4 w-4" />
										Apply Filters
									</button>
								</li>
							</ul>
						</div>
					{/if}
				</div>
			</div>
		</div>
		<div class="flex flex-col gap-y-4 px-6 py-5 lg:gap-y-6">
			<!-- Data -->
			<div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
				{#each liveAlertDummy as liveAlert}
					<div
						class="hover:bg-brand-50 w-full rounded-lg bg-gray-100/70 px-6 py-5 transition duration-300"
					>
						<div class="flex flex-col gap-y-4 lg:flex-row lg:items-center lg:justify-between">
							<div class="flex items-center gap-x-3">
								<div class="bg-brand-500 flex h-11 w-11 items-center justify-center rounded-full">
									<liveAlert.icon class="h-6 w-6 text-white" />
								</div>
								<div class="flex flex-col gap-y-1">
									<p class="text-theme-md font-medium text-gray-800">{liveAlert.title}</p>
									<div class="flex items-center gap-x-4">
										<div class="flex items-center gap-x-1">
											<Clock class="h-4 w-4 text-gray-400" />
											<span class="text-theme-sm text-gray-400">{liveAlert.time}</span>
										</div>
										<div class="flex items-center gap-x-1">
											<MapPin class="h-4 w-4 text-gray-400" />
											<span class="text-theme-sm text-gray-400">{liveAlert.location}</span>
										</div>
									</div>
								</div>
							</div>
							<div class="flex items-center gap-x-2">
								<button
									aria-label="checkButton"
									class="btn-secondary-icon"
								>
									<Check class="h-4 w-4" />
								</button>
								<button
									aria-label="maximizeButton"
									class="btn-secondary-icon"
								>
									<Maximize class="h-4 w-4" />
								</button>
							</div>
						</div>
					</div>
				{/each}
			</div>
			<!-- Pagination -->
			<div class="flex flex-col items-center gap-y-4 lg:flex-row lg:justify-between">
				<span class="text-theme-sm text-gray-400">Showing 10 to 10 of 30 entries</span>
				<div class="flex items-center gap-x-3">
					<button aria-label="previousButton" class="btn-secondary-icon">
						<ChevronLeft class="h-5 w-5" />
					</button>
					<div class="flex items-center gap-x-1">
						<button
							aria-label="pageButton"
							class="pagination-page text-brand-500 bg-blue-500/[0.08]">1</button
						>
						<button aria-label="pageButton" class="pagination-page">2</button>
					</div>
					<button aria-label="nextButton" class="btn-secondary-icon">
						<ChevronRight class="h-5 w-5" />
					</button>
				</div>
				<div class="flex items-center gap-x-2">
					<span class="text-theme-sm text-gray-400">rows per page</span>
					<div class="relative z-20 bg-transparent">
						<select class="select-input">
							{#each [10, 20, 30, 40, 50] as perRows}
								<option value={perRows} class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">
									{perRows}
								</option>
							{/each}
						</select>
						<span
							class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
						>
							<ChevronDown class="h-5 w-5" />
						</span>
					</div>
				</div>
			</div>
		</div>
	</div>
	<!-- Notification Settings -->
	<div
		class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
	>
		<div
			class="flex flex-col gap-y-2 border-b border-gray-100 px-6 py-5 md:flex-row md:items-center md:justify-between dark:border-gray-800"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Notification Settings</h3>
		</div>
		<div class="flex flex-col gap-y-6 px-6 py-5">
			<div class="grid grid-cols-1 gap-y-4 lg:grid-cols-2 lg:gap-x-8">
				<!-- Alert Types -->
				<div class="flex flex-col gap-y-4">
					<p class="text-theme-md font-medium text-gray-800">Alert Types</p>
					<div class="flex flex-col gap-y-4">
						<!-- Motion Detection -->
						<div class="flex items-center justify-between">
							<label
								for="checkboxLabelOne"
								class="flex cursor-pointer items-center text-sm font-medium text-gray-700 select-none dark:text-gray-400"
							>
								<div class="relative">
									<input
										type="checkbox"
										id="checkboxLabelOne"
										class="sr-only"
										bind:checked={checkboxToggle}
									/>
									<div
										class={`hover:border-brand-500 dark:hover:border-brand-500 mr-3 flex h-5 w-5 items-center justify-center rounded-md border-[1.25px] ${checkboxToggle ? 'border-brand-500 bg-brand-500' : 'border-gray-300 bg-transparent dark:border-gray-700'}`}
									>
										<span class={checkboxToggle ? '' : 'opacity-0'}>
											<Check class="h-4 w-4 text-white" />
										</span>
									</div>
								</div>
								Motion Detection
							</label>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Medium', 'Low', 'High'] as option}
										<option
											value={option}
											class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>
											{option}
										</option>
									{/each}
								</select>
								<span
									class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
								>
									<ChevronDown class="h-5 w-5" />
								</span>
							</div>
						</div>
						<!-- Face Recognition -->
						<div class="flex items-center justify-between">
							<label
								for="checkboxLabelOne"
								class="flex cursor-pointer items-center text-sm font-medium text-gray-700 select-none dark:text-gray-400"
							>
								<div class="relative">
									<input
										type="checkbox"
										id="checkboxLabelOne"
										class="sr-only"
										bind:checked={checkboxToggle}
									/>
									<div
										class={`hover:border-brand-500 dark:hover:border-brand-500 mr-3 flex h-5 w-5 items-center justify-center rounded-md border-[1.25px] ${checkboxToggle ? 'border-brand-500 bg-brand-500' : 'border-gray-300 bg-transparent dark:border-gray-700'}`}
									>
										<span class={checkboxToggle ? '' : 'opacity-0'}>
											<Check class="h-4 w-4 text-white" />
										</span>
									</div>
								</div>
								Face Recognition
							</label>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Medium', 'Low', 'High'] as option}
										<option
											value={option}
											class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>
											{option}
										</option>
									{/each}
								</select>
								<span
									class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
								>
									<ChevronDown class="h-5 w-5" />
								</span>
							</div>
						</div>
						<!-- Intrusion Detection -->
						<div class="flex items-center justify-between">
							<label
								for="checkboxLabelOne"
								class="flex cursor-pointer items-center text-sm font-medium text-gray-700 select-none dark:text-gray-400"
							>
								<div class="relative">
									<input
										type="checkbox"
										id="checkboxLabelOne"
										class="sr-only"
										bind:checked={checkboxToggle}
									/>
									<div
										class={`hover:border-brand-500 dark:hover:border-brand-500 mr-3 flex h-5 w-5 items-center justify-center rounded-md border-[1.25px] ${checkboxToggle ? 'border-brand-500 bg-brand-500' : 'border-gray-300 bg-transparent dark:border-gray-700'}`}
									>
										<span class={checkboxToggle ? '' : 'opacity-0'}>
											<Check class="h-4 w-4 text-white" />
										</span>
									</div>
								</div>
								Intrusion Detection
							</label>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Medium', 'Low', 'High'] as option}
										<option
											value={option}
											class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>
											{option}
										</option>
									{/each}
								</select>
								<span
									class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
								>
									<ChevronDown class="h-5 w-5" />
								</span>
							</div>
						</div>
						<!-- Unattended Object -->
						<div class="flex items-center justify-between">
							<label
								for="checkboxLabelOne"
								class="flex cursor-pointer items-center text-sm font-medium text-gray-700 select-none dark:text-gray-400"
							>
								<div class="relative">
									<input
										type="checkbox"
										id="checkboxLabelOne"
										class="sr-only"
										bind:checked={checkboxToggle}
									/>
									<div
										class={`hover:border-brand-500 dark:hover:border-brand-500 mr-3 flex h-5 w-5 items-center justify-center rounded-md border-[1.25px] ${checkboxToggle ? 'border-brand-500 bg-brand-500' : 'border-gray-300 bg-transparent dark:border-gray-700'}`}
									>
										<span class={checkboxToggle ? '' : 'opacity-0'}>
											<Check class="h-4 w-4 text-white" />
										</span>
									</div>
								</div>
								Unattended Object
							</label>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Medium', 'Low', 'High'] as option}
										<option
											value={option}
											class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>
											{option}
										</option>
									{/each}
								</select>
								<span
									class="pointer-events-none absolute top-1/2 right-4 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400"
								>
									<ChevronDown class="h-5 w-5" />
								</span>
							</div>
						</div>
					</div>
				</div>
				<!-- Notification Methods -->
				<div class="flex flex-col gap-y-4">
					<p class="text-theme-md font-medium text-gray-800">Notification Methods</p>
					<div class="flex flex-col gap-y-4">
						<!-- In-App Notifications -->
						<label
							for="checkboxLabelOne"
							class="flex cursor-pointer items-center text-sm font-medium text-gray-700 select-none dark:text-gray-400"
						>
							<div class="relative">
								<input
									type="checkbox"
									id="checkboxLabelOne"
									class="sr-only"
									bind:checked={checkboxToggle}
								/>
								<div
									class={`hover:border-brand-500 dark:hover:border-brand-500 mr-3 flex h-5 w-5 items-center justify-center rounded-md border-[1.25px] ${checkboxToggle ? 'border-brand-500 bg-brand-500' : 'border-gray-300 bg-transparent dark:border-gray-700'}`}
								>
									<span class={checkboxToggle ? '' : 'opacity-0'}>
										<Check class="h-4 w-4 text-white" />
									</span>
								</div>
							</div>
							In-App Notifications
						</label>
						<!-- Email Notifications -->
						<label
							for="checkboxLabelOne"
							class="flex cursor-pointer items-center text-sm font-medium text-gray-700 select-none dark:text-gray-400"
						>
							<div class="relative">
								<input
									type="checkbox"
									id="checkboxLabelOne"
									class="sr-only"
									bind:checked={checkboxToggle}
								/>
								<div
									class={`hover:border-brand-500 dark:hover:border-brand-500 mr-3 flex h-5 w-5 items-center justify-center rounded-md border-[1.25px] ${checkboxToggle ? 'border-brand-500 bg-brand-500' : 'border-gray-300 bg-transparent dark:border-gray-700'}`}
								>
									<span class={checkboxToggle ? '' : 'opacity-0'}>
										<Check class="h-4 w-4 text-white" />
									</span>
								</div>
							</div>
							Email Notifications
						</label>
						<!-- SMS Notifications -->
						<label
							for="checkboxLabelOne"
							class="flex cursor-pointer items-center text-sm font-medium text-gray-700 select-none dark:text-gray-400"
						>
							<div class="relative">
								<input
									type="checkbox"
									id="checkboxLabelOne"
									class="sr-only"
									bind:checked={checkboxToggle}
								/>
								<div
									class={`hover:border-brand-500 dark:hover:border-brand-500 mr-3 flex h-5 w-5 items-center justify-center rounded-md border-[1.25px] ${checkboxToggle ? 'border-brand-500 bg-brand-500' : 'border-gray-300 bg-transparent dark:border-gray-700'}`}
								>
									<span class={checkboxToggle ? '' : 'opacity-0'}>
										<Check class="h-4 w-4 text-white" />
									</span>
								</div>
							</div>
							SMS Notifications
						</label>
						<!-- Sound Alerts -->
						<label
							for="checkboxLabelOne"
							class="flex cursor-pointer items-center text-sm font-medium text-gray-700 select-none dark:text-gray-400"
						>
							<div class="relative">
								<input
									type="checkbox"
									id="checkboxLabelOne"
									class="sr-only"
									bind:checked={checkboxToggle}
								/>
								<div
									class={`hover:border-brand-500 dark:hover:border-brand-500 mr-3 flex h-5 w-5 items-center justify-center rounded-md border-[1.25px] ${checkboxToggle ? 'border-brand-500 bg-brand-500' : 'border-gray-300 bg-transparent dark:border-gray-700'}`}
								>
									<span class={checkboxToggle ? '' : 'opacity-0'}>
										<Check class="h-4 w-4 text-white" />
									</span>
								</div>
							</div>
							Sound Alerts
						</label>
					</div>
				</div>
			</div>
			<div class="flex justify-end">
				<button class="btn-primary-md">
					<Save class="h-5 w-5" />
					Save Settings
				</button>
			</div>
		</div>
	</div>
</div>
