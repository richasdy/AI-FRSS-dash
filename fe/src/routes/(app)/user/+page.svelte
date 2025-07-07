<script lang="ts">
	import { createQuery } from '@tanstack/svelte-query';
	import { getAllUsers } from './api';
	import Breadcrumb from '../../../components/breadcrumb/Breadcrumb.svelte';
	import { roleDummy } from './data';
	import { approveUser, rejectUser, deleteUser } from './api';

	import {
	Check,
		ChevronDown,
		ChevronLeft,
		ChevronRight,
		Download,
		Filter,
		Key,
		PencilLine,
		Plus,
		ShieldUser,
		Trash,
		UserCheck,
		Users,
		UserSearch,

		X

	} from '@lucide/svelte';
	import Badge from '../../../components/badge/Badge.svelte';
	import { slide } from 'svelte/transition';
	import { queryClient } from '$lib/queryClient';

  let openUserFilters = false;
  let searchUsers = '';

  const usersQuery = createQuery({
    queryKey: ['users', searchUsers],
    queryFn: () => getAllUsers(searchUsers)
  });

  // ✅ log di reactive statement
  $: if ($usersQuery.data) {
    console.log('Users data:', $usersQuery.data);
  }



</script>

<div class="flex flex-col gap-y-6">
	<Breadcrumb pageName="User Management" />
	<!-- User Stats -->
	<div class="grid grid-cols-1 gap-2 md:grid-cols-2 lg:grid-cols-4 lg:gap-4">
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-brand-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<Users class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">100</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Total Users</p>
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
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">20</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Active Now</p>
				</div>
			</div>
		</div>
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-error-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<ShieldUser class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">30</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Administrator</p>
				</div>
			</div>
		</div>
		<div
			class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
		>
			<div class="flex items-center gap-x-4">
				<div class="bg-brand-500 flex h-14 w-14 items-center justify-center rounded-lg">
					<UserSearch class="h-6 w-6 text-white" />
				</div>
				<div class="flex flex-col">
					<p class="text-theme-lg font-semibold text-gray-800 dark:text-white/90">50</p>
					<p class="text-theme-sm text-gray-500 dark:text-white/70">Pending Approval</p>
				</div>
			</div>
		</div>
	</div>
	<!-- User Management -->
	<div
		class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
	>
		<div
			class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-3 lg:flex-row lg:items-center lg:justify-between dark:border-gray-800"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">User Management</h3>
			<div class="flex flex-wrap items-center gap-x-2 gap-y-2">
				<button class="btn-primary-sm" aria-label="downloadButton">
					<Plus class="h-4 w-4" />
					Add User
				</button>
				<button class="btn-secondary-outline-md" aria-label="downloadButton">
					<Download class="h-4 w-4" />
					Export Data
				</button>
				<!-- Filters -->
				<div class="relative inline-block">
					<button
						onclick={() => (openUserFilters = !openUserFilters)}
						aria-label="exportButton"
						class="btn-primary-outline-sm"
					>
						<Filter class="h-4 w-4" />
						Filters
					</button>
					{#if openUserFilters}
						<div class="dropdown" transition:slide>
							<ul class="flex flex-col gap-y-2">
								<li class="form-groups">
									<span class="form-label">Role</span>
									<div class="relative z-20 bg-transparent">
										<select class="select-input">
											<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>Select option</option
											>
											{#each ['Admin', 'Manager', 'User'] as option}
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
								<li class="form-groups">
									<span class="form-label">Role</span>
									<div class="relative z-20 bg-transparent">
										<select class="select-input">
											<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>Select option</option
											>
											{#each ['Online', 'Offile'] as option}
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
								<li class="form-groups">
									<span class="form-label">Approvall</span>
									<div class="relative z-20 bg-transparent">
										<select class="select-input">
											<option value="" class="text-gray-700 dark:bg-gray-900 dark:text-gray-400"
												>Select option</option
											>
											{#each ['Approved', 'Rejected', 'Pending'] as option}
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
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Name</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Email</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Role</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">
										Department
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
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Approval</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">
										Last Login
									</p>
								</div>
							</th>
						</tr>
					</thead>
					<!-- Table Header -->

					<!-- Table Body -->
					<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
						{#if $usersQuery.isLoading}
						  <tr>
							<td colspan="9" class="p-4 text-center">Loading...</td>
						  </tr>
						{:else if $usersQuery.isError}
						  <tr>
							<td colspan="9" class="p-4 text-center">Error loading users</td>
						  </tr>
						{:else}
						  {#each $usersQuery.data as user, index}
							<tr>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center">
								  <p class="text-theme-sm text-gray-500 dark:text-gray-400">{index + 1}</p>
								</div>
							  </td>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center">
								  <p class="text-theme-sm text-gray-500 dark:text-gray-400">{user.name}</p>
								</div>
							  </td>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center">
								  <p class="text-theme-sm text-gray-500 dark:text-gray-400">{user.email}</p>
								</div>
							  </td>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center">
								  <Badge
									type={user.role === 'Admin' ? 'primary' : user.role === 'User' ? 'success' : 'warning'}
									text={user.role}
								  />
								</div>
							  </td>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center">
								  <p class="text-theme-sm text-gray-500 dark:text-gray-400">{user.department}</p>
								</div>
							  </td>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center gap-x-1">
								  <div
									class={`h-2 w-2 rounded-full ${user.isOnline ? 'bg-success-500' : 'bg-error-500'}`}
								  ></div>
								  <span class="text-theme-sm text-gray-500 dark:text-gray-400">
									{user.isOnline ? 'Online' : 'Offline'}
								  </span>
								</div>
							  </td>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center">
								  <p
									class={`text-theme-sm ${user.isApproved ? 'text-success-500' : 'text-error-500'}`}
								  >
									{user.isApproved ? 'Approved' : 'Pending'}
								  </p>
								</div>
							  </td>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center">
								  <p class="text-theme-sm text-gray-500 dark:text-gray-400">{user.lastLogin}</p>
								</div>
							  </td>
							  <td class="px-5 py-4 sm:px-6">
								<div class="flex items-center gap-x-2">
									{#if user.isApproved}
										<button aria-label="actionButton" class="btn-secondary-icon">
											<PencilLine class="h-4 w-4" />
										</button>
										<button aria-label="actionButton" class="btn-secondary-icon">
											<Key class="h-4 w-4" />
										</button>
										<button
											aria-label="actionButton"
											class="btn-secondary-icon"
											onclick={async () => {
												await deleteUser(user.id);
												await queryClient.invalidateQueries({ queryKey: ['users', searchUsers] });
											}}
										>
											<Trash class="h-4 w-4" />
										</button>
									{:else}
										<button
											aria-label="actionButton"
											class="btn-secondary-icon"
											onclick={async () => {
												await approveUser(user.id);
												await queryClient.invalidateQueries({ queryKey: ['users', searchUsers] });
											}}
										>
											<Check class="h-4 w-4" />
										</button>
										<button
											aria-label="actionButton"
											class="btn-secondary-icon"
											onclick={async () => {
												await rejectUser(user.id);
												await queryClient.invalidateQueries({ queryKey: ['users', searchUsers] });
											}}
										>
											<X class="h-4 w-4" />
										</button>
									{/if}
								</div>
							</td>							
							</tr>
						  {/each}
						{/if}
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
	<!-- Role Management -->
	<div
		class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
	>
		<div
			class="flex flex-col gap-y-4 border-b border-gray-100 px-6 py-3 lg:flex-row lg:items-center lg:justify-between dark:border-gray-800"
		>
			<h3 class="text-base font-medium text-gray-800 dark:text-white/90">Role Management</h3>
			<div class="flex flex-wrap items-center gap-x-2 gap-y-2">
				<button class="btn-primary-sm" aria-label="downloadButton">
					<Plus class="h-4 w-4" />
					Add Role
				</button>
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
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Name</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Users</p>
								</div>
							</th>
							<th class="px-5 py-3 sm:px-6">
								<div class="flex items-center">
									<p class="text-theme-xs font-medium text-gray-500 dark:text-gray-400">Permissions</p>
								</div>
							</th>
						</tr>
					</thead>
					<!-- Table Header -->

					<!-- Table Body -->
					<tbody class="divide-y divide-gray-100 dark:divide-gray-800">
						{#each roleDummy as role, index}
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
										<Badge
											type={role.name === 'Admin'
												? 'primary'
												: role.name === 'User'
													? 'success'
													: 'warning'}
											text={role.name}
										/>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{role.users}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center">
										<p class="text-theme-sm text-gray-500 dark:text-gray-400">
											{role.name}
										</p>
									</div>
								</td>
								<td class="px-5 py-4 sm:px-6">
									<div class="flex items-center gap-x-2">
										<button aria-label="actionButton" class="btn-secondary-icon">
											<PencilLine class="h-4 w-4" />
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
