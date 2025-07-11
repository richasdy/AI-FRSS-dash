<script lang="ts">
	import { onMount } from 'svelte';
	import { slide } from 'svelte/transition';

	export let sidebarToggle: boolean;
	export let menuToggle: boolean;

	let openUserDropdown: boolean = false;
	let userProfile: User | null = null;

	const handleLogout = () => {
		localStorage.removeItem('accessToken');
		localStorage.removeItem('userProfile');
		window.location.href = '/signin';
	};

	onMount(() => {
		const storedUserProfile = localStorage.getItem('userProfile');

		if (storedUserProfile) {
			userProfile = JSON.parse(storedUserProfile);
		}
	});
</script>

<header
	class="sticky top-0 z-99999 flex w-full border-gray-200 bg-white lg:border-b dark:border-gray-800 dark:bg-gray-900"
>
	<div class="flex grow flex-col items-center justify-between lg:flex-row lg:px-6">
		<!-- Left content -->
		<div
			class="flex w-full items-center justify-between gap-2 border-b border-gray-200 px-3 py-3 sm:gap-4 lg:justify-normal lg:border-b-0 lg:px-0 lg:py-4 dark:border-gray-800"
		>
			<!-- Hamburger Toggle BTN -->
			<button
				class={`z-99999 flex h-10 w-10 items-center justify-center rounded-lg border-gray-200 text-gray-500 lg:h-11 lg:w-11 lg:border dark:border-gray-800 dark:text-gray-400 ${sidebarToggle ? 'bg-gray-100 lg:bg-transparent dark:bg-gray-800 dark:lg:bg-transparent' : ''}`}
				on:click={() => (sidebarToggle = !sidebarToggle)}
			>
				<svg
					class="hidden fill-current lg:block"
					width="16"
					height="12"
					viewBox="0 0 16 12"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						fill-rule="evenodd"
						clip-rule="evenodd"
						d="M0.583252 1C0.583252 0.585788 0.919038 0.25 1.33325 0.25H14.6666C15.0808 0.25 15.4166 0.585786 15.4166 1C15.4166 1.41421 15.0808 1.75 14.6666 1.75L1.33325 1.75C0.919038 1.75 0.583252 1.41422 0.583252 1ZM0.583252 11C0.583252 10.5858 0.919038 10.25 1.33325 10.25L14.6666 10.25C15.0808 10.25 15.4166 10.5858 15.4166 11C15.4166 11.4142 15.0808 11.75 14.6666 11.75L1.33325 11.75C0.919038 11.75 0.583252 11.4142 0.583252 11ZM1.33325 5.25C0.919038 5.25 0.583252 5.58579 0.583252 6C0.583252 6.41421 0.919038 6.75 1.33325 6.75L7.99992 6.75C8.41413 6.75 8.74992 6.41421 8.74992 6C8.74992 5.58579 8.41413 5.25 7.99992 5.25L1.33325 5.25Z"
						fill=""
					/>
				</svg>

				<svg
					class={`fill-current lg:hidden ${sidebarToggle ? 'hidden' : 'block lg:hidden'}`}
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						fill-rule="evenodd"
						clip-rule="evenodd"
						d="M3.25 6C3.25 5.58579 3.58579 5.25 4 5.25L20 5.25C20.4142 5.25 20.75 5.58579 20.75 6C20.75 6.41421 20.4142 6.75 20 6.75L4 6.75C3.58579 6.75 3.25 6.41422 3.25 6ZM3.25 18C3.25 17.5858 3.58579 17.25 4 17.25L20 17.25C20.4142 17.25 20.75 17.5858 20.75 18C20.75 18.4142 20.4142 18.75 20 18.75L4 18.75C3.58579 18.75 3.25 18.4142 3.25 18ZM4 11.25C3.58579 11.25 3.25 11.5858 3.25 12C3.25 12.4142 3.58579 12.75 4 12.75L12 12.75C12.4142 12.75 12.75 12.4142 12.75 12C12.75 11.5858 12.4142 11.25 12 11.25L4 11.25Z"
						fill=""
					/>
				</svg>

				<!-- cross icon -->
				<svg
					class={`fill-current ${sidebarToggle ? 'block lg:hidden' : 'hidden'}`}
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						fill-rule="evenodd"
						clip-rule="evenodd"
						d="M6.21967 7.28131C5.92678 6.98841 5.92678 6.51354 6.21967 6.22065C6.51256 5.92775 6.98744 5.92775 7.28033 6.22065L11.999 10.9393L16.7176 6.22078C17.0105 5.92789 17.4854 5.92788 17.7782 6.22078C18.0711 6.51367 18.0711 6.98855 17.7782 7.28144L13.0597 12L17.7782 16.7186C18.0711 17.0115 18.0711 17.4863 17.7782 17.7792C17.4854 18.0721 17.0105 18.0721 16.7176 17.7792L11.999 13.0607L7.28033 17.7794C6.98744 18.0722 6.51256 18.0722 6.21967 17.7794C5.92678 17.4865 5.92678 17.0116 6.21967 16.7187L10.9384 12L6.21967 7.28131Z"
						fill=""
					/>
				</svg>
			</button>
			<!-- Hamburger Toggle BTN -->

			<a href="/" class="lg:hidden">
				<img class="dark:hidden" src="logo/logo.svg" alt="Logo" />
				<img class="hidden dark:block" src="logo/logo-dark.svg" alt="Logo" />
			</a>

			<!-- Application nav menu button -->
			<button
				class={`z-99999 flex h-10 w-10 items-center justify-center rounded-lg text-gray-700 hover:bg-gray-100 lg:hidden dark:text-gray-400 dark:hover:bg-gray-800 ${menuToggle ? 'bg-gray-100 dark:bg-gray-800' : ''}`}
				on:click={() => (menuToggle = !menuToggle)}
				aria-label="Menu Toggle"
			>
				<svg
					class="fill-current"
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						fill-rule="evenodd"
						clip-rule="evenodd"
						d="M5.99902 10.4951C6.82745 10.4951 7.49902 11.1667 7.49902 11.9951V12.0051C7.49902 12.8335 6.82745 13.5051 5.99902 13.5051C5.1706 13.5051 4.49902 12.8335 4.49902 12.0051V11.9951C4.49902 11.1667 5.1706 10.4951 5.99902 10.4951ZM17.999 10.4951C18.8275 10.4951 19.499 11.1667 19.499 11.9951V12.0051C19.499 12.8335 18.8275 13.5051 17.999 13.5051C17.1706 13.5051 16.499 12.8335 16.499 12.0051V11.9951C16.499 11.1667 17.1706 10.4951 17.999 10.4951ZM13.499 11.9951C13.499 11.1667 12.8275 10.4951 11.999 10.4951C11.1706 10.4951 10.499 11.1667 10.499 11.9951V12.0051C10.499 12.8335 11.1706 13.5051 11.999 13.5051C12.8275 13.5051 13.499 12.8335 13.499 12.0051V11.9951Z"
						fill=""
					/>
				</svg>
			</button>
			<!-- Application nav menu button -->
		</div>
		<!-- Left content -->

		<!-- Right content -->
		<div
			class={`shadow-theme-md w-full items-center justify-between gap-4 px-5 py-4 lg:flex lg:justify-end lg:px-0 lg:shadow-none ${menuToggle ? 'flex' : 'hidden'}`}
		>
			<!-- User area -->
			<div class="relative">
				<button
					class="flex items-center text-gray-700 dark:text-gray-400"
					aria-label="User Menu Dropdown Button"
					on:click={() => (openUserDropdown = !openUserDropdown)}
				>
					<span
						class="mr-3 flex h-11 w-11 items-center justify-center overflow-hidden rounded-full border border-gray-200 dark:border-gray-800"
					>
						{userProfile?.name[0] ?? 'U'}
					</span>

					<span class="text-theme-sm mr-1 block font-medium">{userProfile?.name ?? 'Unknown'}</span>

					<svg
						class={`stroke-gray-500 transition duration-300 dark:stroke-gray-400 ${openUserDropdown ? 'rotate-180' : ''}`}
						width="18"
						height="20"
						viewBox="0 0 18 20"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M4.3125 8.65625L9 13.3437L13.6875 8.65625"
							stroke=""
							stroke-width="1.5"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</button>

				{#if openUserDropdown}
					<div
						class="shadow-theme-lg dark:bg-gray-dark absolute right-0 mt-[17px] flex w-[260px] flex-col rounded-2xl border border-gray-200 bg-white p-3 dark:border-gray-800"
						transition:slide
					>
						<div>
							<span class="text-theme-sm block font-medium text-gray-700 dark:text-gray-400">
								{userProfile?.name ?? 'Unknown'}
							</span>
							<span class="text-theme-xs mt-0.5 block text-gray-500 dark:text-gray-400">
								{userProfile?.email ?? 'Unknown email'}
							</span>
						</div>
						<ul class="flex flex-col gap-1 pt-4 pb-3">
							<li>
								<button
									type="button"
									on:click={handleLogout}
									class="group text-theme-sm flex w-full items-center gap-3 rounded-lg px-3 py-2 font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="size-5"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9"
										/>
									</svg>
									Logout
								</button>
							</li>
						</ul>
					</div>
				{/if}
			</div>
			<!-- User area -->
		</div>
		<!-- Right content -->
	</div>
</header>
