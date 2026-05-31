<script lang="ts">
  import { Select as SelectPrimitive } from 'bits-ui';

  // Typed as single-select only (string value); all usages in this app are single-select.
  type SingleSelectProps = Omit<SelectPrimitive.RootProps, 'type' | 'value' | 'onValueChange'> & {
    value?: string;
    onValueChange?: (value: string) => void;
  };

  let {
    open = $bindable(false),
    value = $bindable(''),
    ...restProps
  }: SingleSelectProps = $props();
</script>

<SelectPrimitive.Root type="single" bind:open bind:value={value as never} {...restProps} />
