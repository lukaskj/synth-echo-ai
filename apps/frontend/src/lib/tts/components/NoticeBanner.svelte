<script lang="ts">
  import type { Snippet } from 'svelte';

  type NoticeTone = 'error' | 'success' | 'neutral' | 'muted';

  type Props = {
    tone?: NoticeTone;
    className?: string;
    role?: string;
    children?: Snippet;
  };

  const toneClasses: Record<NoticeTone, string> = {
    error: 'border-rose-500/30 bg-rose-500/10 text-rose-100',
    success: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-100',
    neutral: 'border-slate-800 bg-slate-950/60 text-slate-300',
    muted: 'border-dashed border-slate-700 bg-slate-900/50 text-slate-400'
  };

  let { tone = 'neutral', className = '', role, children }: Props = $props();
</script>

<div class={`rounded-lg border text-sm leading-6 ${toneClasses[tone]} ${className}`.trim()} {role}>
  {@render children?.()}
</div>
