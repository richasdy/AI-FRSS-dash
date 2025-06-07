<script lang="ts">
	import {
		Camera,
		Check,
		CheckCircle,
		ChevronDown,
		ChevronLeft,
		ChevronRight,
		Download,
		Filter,
		Info,
		PencilLine,
		Plus,
		RefreshCcw,
		Save,
		Settings,
		Trash,
		XCircle
	} from '@lucide/svelte';
	import Breadcrumb from '../../../components/breadcrumb/Breadcrumb.svelte';
	import { cameraDummy } from './data';
	import { slide } from 'svelte/transition';
	import { monitoringDummy } from '../live-monitoring/data';

	let openCameraFilters = $state(false);
	let searchCamera = $state('');
	let checkboxToggle = $state(false);
</script>

<div class="flex flex-col gap-y-6">
	<Breadcrumb pageName="Camera Management" />
	<!-- Camera Stats -->
	<div class="grid grid-cols-1 gap-2 md:grid-cols-2 lg:grid-cols-4 lg:gap-4">
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-brand-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<Camera class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">100</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Total Cameras</p>
				</div>
			</div>
		</div>
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-success-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<CheckCircle class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">20</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Online Cameras</p>
				</div>
			</div>
		</div>
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-error-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<XCircle class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">30</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Offline Cameras</p>
				</div>
			</div>
		</div>
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-brand-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<Info class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">50</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Maintenance Cameras</p>
				</div>
			</div>
		</div>
	</div>
	<!-- Data -->
	<div class="rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
		<div
			class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-3 lg:flex-row lg:items-center lg:justify-between dark:border-gray-800"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Camera Management</h3>
			<div class="flex flex-wrap items-center gap-x-2 gap-y-2">
				<input
					type="text"
					placeholder="Search camera"
					bind:value={searchCamera}
					class="text-input w-full lg:w-fit"
				/>
				<button class="btn-primary-sm" aria-label="downloadButton">
					<Plus class="h-4 w-4" />
					Add Camera
				</button>
				<button class="btn-secondary-outline-md" aria-label="downloadButton">
					<Download class="h-4 w-4" />
					Export Data
				</button>
				<!-- Filters -->
				<div class="relative inline-block">
					<button
						onclick={() => (openCameraFilters = !openCameraFilters)}
						aria-label="exportButton"
						class="btn-primary-outline-sm"
					>
						<Filter class="h-4 w-4" />
						Filters
					</button>
					{#if openCameraFilters}
						<div class="dropdown" transition:slide>
							<ul class="flex flex-col gap-y-2">
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
								<li class="form-groups">
									<span class="form-label">Status</span>
									<div class="relative z-20 bg-transparent">
										<select class="select-input">
											<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>Select option</option
											>
											{#each ['Online', 'Offline'] as option}
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
								<li class="mt-4 flex items-center justify-end gap-x-2">
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
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">ID</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Name</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Location</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">
										IP Address
									</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Status</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">
										Last Updated
									</p>
								</div>
							</th>
						</tr>
					</thead>
					<!-- Table Header -->

					<!-- Table Body -->
					<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
						{#each cameraDummy as camera, index}
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
											{camera.id}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{camera.name}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{camera.location}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{camera.ipAddress}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center gap-x-1">
										<div
											class={`h-2 w-2 rounded-full ${camera.isOnline ? 'bg-success-500' : 'bg-error-500'}`}
										></div>
										<span class="text-theme-sm text-gray-500 dark:text-gray-400">
											{camera.isOnline ? 'Online' : 'Offline'}
										</span>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{camera.lastUpdated}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center gap-x-2">
										<button aria-label="editButton" class="btn-secondary-icon">
											<PencilLine class="h-4 w-4" />
										</button>
										<button aria-label="settingButton" class="btn-secondary-icon">
											<Settings class="h-4 w-4" />
										</button>
										<button aria-label="deleteButton" class="btn-secondary-icon">
											<Trash class="h-4 w-4" />
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
	<!-- Settings -->
	<div class="rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
		<div
			class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-5 lg:flex-row lg:items-center lg:justify-between dark:border-gray-800"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Camera Settings</h3>
		</div>
		<div class="flex flex-col gap-y-6 px-6 py-5">
			<div class="grid grid-cols-1 gap-y-4 md:grid-cols-2 md:gap-x-6 lg:grid-cols-3 lg:gap-x-8">
				<!-- Storage Settings -->
				<div class="flex flex-col gap-y-4">
					<p class="text-theme-md font-medium text-gray-800">Storage Settings</p>
					<div class="flex flex-col gap-y-4">
						<div class="form-groups">
							<span class="form-label">Retention Period</span>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['7 Days', '14 Days', '30 Days'] as option}
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
						<div class="form-groups">
							<span class="form-label">Storage Location</span>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Local Storage', 'Cloud Storage'] as option}
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
						<div class="form-groups">
							<span class="form-label">Compression Level</span>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Low', 'Medium', 'High'] as option}
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
				<!-- Recording Settings -->
				<div class="flex flex-col gap-y-4">
					<p class="text-theme-md font-medium text-gray-800">Recording Settings</p>
					<div class="flex flex-col gap-y-4">
						<div class="form-groups">
							<span class="form-label">Recording Mode</span>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Motion Detection', 'Scheduled', 'Event Based'] as option}
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
						<div class="form-groups">
							<span class="form-label">Resolution</span>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['720p', '1080p', '4K'] as option}
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
						<div class="form-groups">
							<span class="form-label">Frame Rate</span>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['24fps', '25fps', '30fps'] as option}
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
				<!-- Alert Settings -->
				<div class="flex flex-col gap-y-4">
					<p class="text-theme-md font-medium text-gray-800">Alert Settings</p>
					<div class="flex flex-col gap-y-4">
						<div class="form-groups">
							<span class="form-label">Motion Sensitivity</span>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Low', 'Medium', 'High'] as option}
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
					<div class="flex flex-col gap-y-4">
						<div class="form-groups">
							<span class="form-label">Alert Threshold</span>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>Select option</option
									>
									{#each ['Low', 'Medium', 'High'] as option}
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
						Enable Pre-Recording (5 seconds)
					</label>
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
						Enable Post-Recording (10 seconds)
					</label>
				</div>
			</div>
			<div class="flex justify-end items-center gap-x-2">
				<button class="btn-primary-md">
					<Save class="h-5 w-5" />
					Save Settings
				</button>
				<button class="btn-primary-outline-md">
					<RefreshCcw class="h-5 w-5" />
					Reset to Default
				</button>
			</div>
		</div>
	</div>
</div>
