<script lang="ts">
  type Props = {
    id: string;
    label: string;
    value: number;
    displayValue: string;
    min: number;
    max: number;
    step: number;
  };

  let { id, label, value = $bindable(), displayValue, min, max, step }: Props = $props();
</script>

<div>
  <div class="flex items-center justify-between gap-3">
    <label class="text-sm font-medium text-slate-200" for={id}>{label}</label>
    <span class="text-sm text-slate-300">{displayValue}</span>
  </div>
  <input {id} type="range" {min} {max} {step} bind:value class="mt-4 w-full accent-violet-300" />
</div>
