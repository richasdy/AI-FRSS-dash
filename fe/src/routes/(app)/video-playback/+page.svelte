<script lang="ts">
	import {
		AlertTriangle,
		Camera,
		ChevronDown,
		ChevronFirst,
		ChevronLast,
		ChevronLeft,
		ChevronRight,
		Download,
		Filter,
		Footprints,
		Maximize,
		Play,
		RefreshCcw,
		User,

		Volume2

	} from '@lucide/svelte';
	import Breadcrumb from '../../../components/breadcrumb/Breadcrumb.svelte';
	import { recordingDummy } from './data';
	import { slide } from 'svelte/transition';
	import { monitoringDummy } from '../live-monitoring/data';

	let openRecordingFilters = $state(false);
	let searchPerson = $state('');
</script>

<div class="flex flex-col gap-y-6">
	<Breadcrumb pageName="Video Playback" />
	<!-- Video Playback -->
	<div
		class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
	>
		<div
			class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-3 dark:border-gray-800 lg:flex-row lg:justify-between lg:items-center"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Video Playback</h3>
			<div class="flex flex-wrap items-center gap-y-2 gap-x-2">
				<button class="btn-secondary-outline-md" aria-label="downloadButton">
					<Download class="h-4 w-4" />
					Download
				</button>
				<button class="btn-secondary-outline-md" aria-label="downloadButton">
					<Camera class="h-4 w-4" />
					Snapshot
				</button>
				<button class="btn-secondary-outline-md" aria-label="downloadButton">
					<Maximize class="h-4 w-4" />
					Fullscreen
				</button>
			</div>
		</div>
		<div class="flex flex-col gap-y-8 px-6 py-5">
			<div class="relative h-96 w-full overflow-hidden rounded-lg">
				<img
					src="https://www.computerworld.com/wp-content/uploads/2024/03/google-meet-shutterstock_1903207828-100916819-orig.jpg?quality=50&strip=all"
					alt="Video Playback"
					class="relative h-full w-full object-cover"
				/>
				<div class="absolute top-0 left-0 h-full w-full bg-gray-800/70"></div>
				<div class="absolute bottom-0 px-4 pb-4 w-full">
					<div class="flex flex-col gap-y-4">
                        <p class="text-theme-lg font-medium text-white">Front Gate - April 16, 2025 10:30 AM</p>
						<div class="flex items-center gap-x-4">
							<div class="flex items-center gap-x-2">
								<button aria-label="videoButton" class="btn-secondary-icon text-white hover:text-gray-800">
                                    <ChevronFirst class="h-4 w-4" />
                                </button>
								<button aria-label="videoButton" class="btn-secondary-icon text-white hover:text-gray-800">
                                    <ChevronLeft class="h-4 w-4" />
                                </button>
								<button aria-label="videoButton" class="btn-secondary-icon text-white hover:text-gray-800">
                                    <Play class="h-4 w-4" />
                                </button>
								<button aria-label="videoButton" class="btn-secondary-icon text-white hover:text-gray-800">
                                    <ChevronLast class="h-4 w-4" />
                                </button>
								<button aria-label="videoButton" class="btn-secondary-icon text-white hover:text-gray-800">
                                    <ChevronRight class="h-4 w-4" />
                                </button>
							</div>
                            <div class="flex flex-1 items-center gap-x-2">
                                <span class="text-theme-sm text-white">10:30:15</span>
                                <div class="h-1.5 w-full rounded bg-brand-500"></div>
                                <span class="text-theme-sm text-white">10:45:15</span>
                            </div>
                            <button aria-label="videoButton" class="btn-secondary-icon text-white hover:text-gray-800">
                                <Volume2 class="h-4 w-4" />
                            </button>
						</div>
					</div>
				</div>
			</div>
            <div class="flex flex-col gap-y-2">
                <div class="flex justify-between items-center">
                    <span class="text-theme-sm text-gray-800">05:00</span>
                    <span class="text-theme-sm text-gray-800">07:30</span>
                    <span class="text-theme-sm text-gray-800">10:46</span>
                </div>
                <div class="w-full h-4 rounded bg-gray-100"></div>
                <div class="flex items-center gap-x-4">
                    <div class="flex items-center gap-x-2">
                        <div class="w-3 h-3 rounded-full bg-success-500"></div>
                        <span class="text-theme-sm text-gray-800">Motion</span>
                    </div>
                    <div class="flex items-center gap-x-2">
                        <div class="w-3 h-3 rounded-full bg-brand-500"></div>
                        <span class="text-theme-sm text-gray-800">Face</span>
                    </div>
                    <div class="flex items-center gap-x-2">
                        <div class="w-3 h-3 rounded-full bg-error-500"></div>
                        <span class="text-theme-sm text-gray-800">Intrusion</span>
                    </div>
                </div>
            </div>
		</div>
	</div>
	<!-- Recording List -->
	<div
		class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
	>
		<div
			class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-3 dark:border-gray-800 lg:flex-row lg:items-center lg:justify-between"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Recording List</h3>
			<div class="flex items-center gap-x-2">
				<input
					type="text"
					placeholder="Search by person name"
					bind:value={searchPerson}
					class="text-input"
				/>
				<!-- Filters -->
				<div class="relative inline-block">
					<button
						onclick={() => (openRecordingFilters = !openRecordingFilters)}
						aria-label="exportButton"
						class="btn-primary-outline-sm"
					>
						<Filter class="h-4 w-4" />
						Filters
					</button>
					{#if openRecordingFilters}
						<div class="dropdown" transition:slide>
							<ul class="flex flex-col gap-y-2">
								<li class="grid grid-cols-1 gap-2 lg:grid-cols-2">
									<!-- Camera -->
									<div class="form-groups">
										<span class="form-label">Camera</span>
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
									</div>
									<!-- Date -->
									<div class="form-groups">
										<span class="form-label">Date</span>
										<input type="date" class="text-input" />
									</div>
								</li>
								<li class="grid grid-cols-1 gap-2 lg:grid-cols-2">
									<!-- Time From -->
									<div class="form-groups">
										<span class="form-label">Time From</span>
										<input type="time" class="text-input" />
									</div>
									<!-- Time To -->
									<div class="form-groups">
										<span class="form-label">Time To</span>
										<input type="time" class="text-input" />
									</div>
								</li>
								<li class="grid grid-cols-1 gap-2 lg:grid-cols-2">
									<!-- Event Types -->
									<div class="form-groups col-span-full">
										<span class="form-label">Event Types</span>
										<div class="relative z-20 bg-transparent">
											<select class="select-input">
												<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
													>Select option</option
												>
												{#each ['Face Recognition', 'Unattended Object', 'Motion Detection', 'Intrusion Alert'] as option}
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
								</li>
								<!-- Apply Button -->
								<li class="mt-4 flex items-center justify-end gap-x-2">
									<button class="btn-primary-md">
										<Filter class="h-4 w-4" />
										Apply Filters
									</button>
									<button class="btn-primary-outline-md">
										<RefreshCcw class="h-4 w-4" />
										Reset Filters
									</button>
								</li>
							</ul>
						</div>
					{/if}
				</div>
			</div>
		</div>
		<div class="flex flex-col gap-y-4 px-6 py-5 lg:gap-y-6">
			<!-- Table -->
			<div class="max-w-full overflow-x-auto">
				<table class="min-w-full">
					<!-- Table Header -->
					<thead class="border-b border-gray-100 dark:border-white/[0.05]">
						<tr>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">#</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Camera</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">
										Date & Time
									</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Duration</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">
										Event Type
									</p>
								</div>
							</th>
						</tr>
					</thead>
					<!-- Table Header -->

					<!-- Table Body -->
					<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
						{#each recordingDummy as recording, index}
							<tr>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{index + 1}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{recording.camera}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{recording.dateTime}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{recording.duration}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center gap-x-2">
										{#if recording.eventType === 'Face Recognition'}
											<User class="h-4 w-4" />
										{:else if recording.eventType === 'Intrusion Alert'}
											<AlertTriangle class="h-4 w-4" />
										{:else if recording.eventType === 'Motion Detection'}
											<Footprints class="h-4 w-4" />
										{/if}
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{recording.eventType}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center gap-x-2">
										<button aria-label="checkButton" class="btn-secondary-icon">
											<Play class="h-4 w-4" />
										</button>
										<button aria-label="maximizeButton" class="btn-secondary-icon">
											<Download class="h-4 w-4" />
										</button>
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
					<!-- Table Body -->
				</table>
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
</div>
