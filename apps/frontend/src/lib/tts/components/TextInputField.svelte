<script lang="ts">
  type Props = {
    id: string;
    label: string;
    value: string;
    placeholder?: string;
    type?: string;
    className?: string;
    labelClassName?: string;
    inputClassName?: string;
    disabled?: boolean;
    readonly?: boolean;
  };

  let {
    id,
    label,
    value = $bindable(),
    placeholder = '',
    type = 'text',
    className = '',
    labelClassName = 'block text-sm font-medium text-slate-200',
    inputClassName = 'mt-3 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-base text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30',
    disabled = false,
    readonly = false
  }: Props = $props();
</script>

<div class={className}>
  <label class={labelClassName} for={id}>{label}</label>
  <input {id} {type} bind:value {placeholder} {disabled} {readonly} class={inputClassName} />
</div>
