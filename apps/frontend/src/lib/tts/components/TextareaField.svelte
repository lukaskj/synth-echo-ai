<script lang="ts">
	type Props = {
		id: string;
		label: string;
		value: string;
		rows?: number;
		placeholder?: string;
		className?: string;
		labelClassName?: string;
		textareaClassName?: string;
		disabled?: boolean;
		readonly?: boolean;
	};

	let {
		id,
		label,
		value = $bindable(),
		rows = 4,
		placeholder = '',
		className = '',
		labelClassName = 'block text-sm font-medium text-slate-200',
		textareaClassName =
			'mt-3 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-base leading-7 text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30',
		disabled = false,
		readonly = false
	}: Props = $props();
</script>

<div class={className}>
	<label class={labelClassName} for={id}>{label}</label>
	<textarea
		{id}
		bind:value
		{rows}
		{placeholder}
		disabled={disabled}
		readonly={readonly}
		class={textareaClassName}
	></textarea>
</div>
