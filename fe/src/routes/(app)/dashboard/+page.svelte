<script lang="ts">
	import { AlertCircle, Camera, UserCheck, UserX } from '@lucide/svelte';
	import Breadcrumb from '../../../components/breadcrumb/Breadcrumb.svelte';
	import { eventDummy, systemHealthDummy } from './data';
	import { renderChart } from 'svelte-chart-apex';
	import { activityTimelineChartData, cameraStatusChartData } from './charts';
</script>

<div class="flex flex-col gap-y-6">
	<Breadcrumb pageName="Dashboard" />
	<!-- Dashboard Stats -->
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
					<UserCheck class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">30</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Attendances Today</p>
				</div>
			</div>
		</div>
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-error-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<AlertCircle class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">40</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Alerts Today</p>
				</div>
			</div>
		</div>
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-brand-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<UserX class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">3</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Blacklist Detection</p>
				</div>
			</div>
		</div>
	</div>
	<!-- Chart -->
	<div class="grid grid-cols-12 gap-4">
		<!-- Chart Security Incidents -->
		<div
			class="col-span-full rounded-2xl border border-gray-200 bg-white md:col-span-6 lg:col-span-7 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div
				class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-3 lg:flex-row lg:items-center lg:justify-between dark:border-gray-800"
			>
				<h3 class="text-base font-medium text-gray-800 dark:text-white/90">
					Activity Timeline
				</h3>
				<div class="flex flex-wrap items-center gap-x-2 gap-y-2">
					<button class="btn-secondary-outline-md" aria-label="tabButton"> Today </button>
					<button class="btn-secondary-outline-md" aria-label="tabButton"> Weekly </button>
					<button class="btn-secondary-outline-md" aria-label="tabButton"> Monthly </button>
				</div>
			</div>
			<div use:renderChart={activityTimelineChartData}></div>
		</div>
		<!-- Chart Incidents -->
		<div
			class="col-span-full rounded-2xl border border-gray-200 bg-white md:col-span-6 lg:col-span-5 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div
				class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-5 lg:flex-row lg:items-center lg:justify-between dark:border-gray-800"
			>
				<h3 class="text-base font-medium text-gray-800 dark:text-white/90">
					Camera Status
				</h3>
			</div>
			<div use:renderChart={cameraStatusChartData}></div>
		</div>
	</div>
	<!-- Event & System -->
	<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
		<!-- Event -->
		<div
			class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div
				class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-3 lg:flex-row lg:items-center lg:justify-between dark:border-gray-800"
			>
				<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Recent Events</h3>
				<div class="flex flex-wrap items-center gap-x-2 gap-y-2">
					<a href="/alert-notification" class="btn-secondary-outline-md" aria-label="tabButton">
						View All
					</a>
				</div>
			</div>
			<!-- Table -->
			<div class="max-w-full overflow-x-auto px-6 py-5">
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
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Time</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Status</p>
								</div>
							</th>
						</tr>
					</thead>
					<!-- Table Header -->

					<!-- Table Body -->
					<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
						{#each eventDummy.slice(0, 3) as event, index}
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
											{event.name}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{event.location}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{event.time}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p
											class={`text-theme-sm ${event.status === 'Pending' ? 'text-warning-500' : event.status === 'Resolved' ? 'text-success-500' : 'text-error-500'}`}
										>
											{event.status}
										</p>
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
					<!-- Table Body -->
				</table>
			</div>
		</div>
		<!-- System -->
		<div
			class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div
				class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-5 lg:flex-row lg:items-center lg:justify-between dark:border-gray-800"
			>
				<h3 class="text-base font-medium text-gray-800 dark:text-white/90">System Health</h3>
			</div>
			<div class="px-6 py-5">
				<div class="flex flex-col gap-y-4">
					{#each systemHealthDummy as health}
						<div class="flex flex-col gap-y-3">
							<div class="flex items-center justify-between">
								<p class="text-theme-md font-medium text-gray-800">{health.label}</p>
								<p class="text-theme-sm text-gray-800">{health.percentage}%</p>
							</div>
							<div class="relative h-3 w-full rounded-full bg-gray-200 dark:bg-gray-800">
								<div
									class={`bg-${health.color}-500 absolute left-0 h-full rounded-full`}
									style="width: {health.percentage}%"
								></div>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</div>
</div>
