<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { HTMLButtonAttributes } from 'svelte/elements';

	type ButtonVariant = 'primary' | 'secondary' | 'danger';
	type ButtonSize = 'small' | 'medium' | 'large';

	type Props = Omit<HTMLButtonAttributes, 'children'> & {
		variant?: ButtonVariant;
		size?: ButtonSize;
		children?: Snippet;
	};

	const variantClasses: Record<ButtonVariant, string> = {
		primary:
			'border border-violet-400 bg-violet-400 text-slate-950 hover:bg-violet-300 focus-visible:outline-violet-300',
		secondary:
			'border border-slate-700 bg-slate-900 text-slate-100 hover:border-violet-400/50 hover:bg-slate-950 focus-visible:outline-violet-300',
		danger:
			'border border-rose-500/30 bg-rose-500/10 text-rose-100 hover:bg-rose-500/20 focus-visible:outline-rose-400'
	};

	const sizeClasses: Record<ButtonSize, string> = {
		small: 'rounded-md px-3 py-2 text-sm',
		medium: 'rounded-lg px-4 py-1 text-base',
		large: 'rounded-lg px-4 py-3 text-base'
	};

	let {
		variant = 'secondary',
		size = 'medium',
		type = 'button',
		disabled = false,
		class: className = '',
		children,
		...restProps
	}: Props = $props();
</script>

<button
	{type}
	{disabled}
	class={`inline-flex items-center justify-center font-semibold transition focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-500 ${sizeClasses[size]} ${variantClasses[variant]} ${className}`.trim()}
	{...restProps}
>
	{@render children?.()}
</button>
