<script lang="ts">
	import { Check, ChevronDown, Clock, MapPin, Maximize } from '@lucide/svelte';
	import Breadcrumb from '../../../components/breadcrumb/Breadcrumb.svelte';
	import {
		feedGridTabs,
		gridClassMap,
		liveAlertDummy,
		monitoringDummy,
		panTiltControls,
		presetPositions,
		quickActions,
		zoomControls
	} from './data';

	let feedsGrid: number = $state(2);

	const videoSources = [
	'/video/vid1.mp4',
	'/video/vid2.mp4',
	'/video/vid3.mp4',
	'/video/vid4.mp4',
	'/video/vid5.mp4',
	'/video/vid6.mp4',
	'/video/vid7.mp4',
	'/video/vid8.mp4',
	'/video/vid9.mp4',
	'/video/vid10.mp4'
];



</script>

<div class="flex flex-col gap-y-6">
	<Breadcrumb pageName="Live Monitoring" />
	<!-- Camera Feeds -->
	<div
		class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
	>
		<div
			class="flex flex-col gap-y-2 border-b border-gray-100 px-6 py-4 md:flex-row md:items-center md:justify-between dark:border-gray-800"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Live Camera Feeds</h3>
			<div class="flex items-center gap-x-2">
				{#each feedGridTabs as grid}
					<button
						aria-label={`gridButton-${grid.label}`}
						class={`btn-primary-outline-sm ${feedsGrid === grid.value ? 'bg-brand-500 text-white' : ''}`}
						onclick={() => (feedsGrid = grid.value)}
					>
						<grid.icon class="h-4 w-4" />

						{grid.label}
					</button>
				{/each}
			</div>
		</div>
		<div class={`grid ${gridClassMap[feedsGrid]} gap-2 px-6 py-5`}>
			{#each monitoringDummy as monitoring, i}
				<div
					class={`relative max-h-56 overflow-hidden border border-gray-200 dark:border-gray-800 ${feedsGrid !== 4 ? 'rounded-xl' : 'rounded-lg'}`}
				>
				<video
					src={videoSources[i % videoSources.length]}
					autoplay
					muted
					loop
					playsinline
					class="relative h-full w-full object-cover"
					onerror={() => console.log('Video gagal load')}
				></video>

					<div class="absolute top-0 left-0 h-full w-full bg-gray-800/50"></div>
					<div class="absolute bottom-0 px-4 pb-4">
						<p class="text-theme-lg font-medium text-white">{monitoring.name}</p>
						<div class="flex items-center gap-x-1">
							<div
								class={`h-2 w-2 rounded-full ${monitoring.isOnline ? 'bg-success-500' : 'bg-error-500'}`}
							></div>
							<span class="text-theme-sm text-white">
								{monitoring.isOnline ? 'Online' : 'Offline'}
							</span>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
	<div class="grid-cols 1 grid gap-y-4 lg:grid-cols-2 lg:gap-x-4">
		<!-- Camera Controls -->
		<div
			class="h-fit rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div
				class="flex flex-col gap-y-2 border-b border-gray-100 px-6 py-5 md:flex-row md:items-center md:justify-between dark:border-gray-800"
			>
				<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Camera Controls</h3>
			</div>
			<div class="flex flex-col gap-y-4 px-6 py-5">
				<div class="flex flex-col gap-y-4">
					<div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
						<div class="flex flex-col gap-y-2">
							<p class="text-theme-sm font-medium text-gray-800 dark:text-white/90">Camera</p>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">
										Select Camera
									</option>
									{#each monitoringDummy as monitoring}
										<option
											value={monitoring.name}
											class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>
											{monitoring.name}
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
						<div class="flex flex-col gap-y-2">
							<p class="text-theme-sm font-medium text-gray-800 dark:text-white/90">
								Preset Position
							</p>
							<div class="relative z-20 bg-transparent">
								<select class="select-input">
									<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400">
										Select Preset
									</option>
									{#each presetPositions as preset}
										<option
											value={preset}
											class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
										>
											{preset}
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
					<div class="flex flex-col gap-y-2">
						<p class="text-theme-sm font-medium text-gray-800 dark:text-white/90">
							Pan/Tilt Controls
						</p>
						<div class="flex items-center gap-x-2">
							{#each panTiltControls as control}
								<button
									aria-label={`panTiltButton-${control.label}`}
									class='btn-secondary-icon'
								>
									<control.icon class="h-4 w-4" />
								</button>
							{/each}
						</div>
					</div>
					<div class="flex flex-col gap-y-2">
						<p class="text-theme-sm font-medium text-gray-800 dark:text-white/90">Zoom Controls</p>
						<div class="flex items-center gap-x-2">
							{#each zoomControls as control}
								<button
									aria-label={`zoomButton-${control.label}`}
									class='btn-secondary-outline-md'
								>
									<control.icon class="h-4 w-4" />
									{control.label}
								</button>
							{/each}
						</div>
					</div>
					<div class="flex flex-col gap-y-2">
						<p class="text-theme-sm font-medium text-gray-800 dark:text-white/90">Quick Actions</p>
						<div class="flex items-center gap-x-2">
							{#each quickActions as control}
								<button
									aria-label={`zoomButton-${control.label}`}
									class='btn-primary-outline-sm'
								>
									<control.icon class="h-4 w-4" />
									{control.label}
								</button>
							{/each}
						</div>
					</div>
				</div>
			</div>
		</div>
		<!-- Live Alerts -->
		<div
			class="h-fit rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div
				class="flex flex-col gap-y-2 border-b border-gray-100 px-6 py-3 md:flex-row md:items-center md:justify-between dark:border-gray-800"
			>
				<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Live Alerts</h3>
				<a
					href="/alert-notification"
					class='btn-secondary-outline-md'
				>
					View All
				</a>
			</div>
			<div class="grid grid-cols-1 gap-y-2 px-6 py-5">
				{#each liveAlertDummy.slice(0, 3) as liveAlert}
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
		</div>
	</div>
</div>
