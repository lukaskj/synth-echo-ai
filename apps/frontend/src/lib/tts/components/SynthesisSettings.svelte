<script lang="ts">
  import * as Select from '$lib/components/ui/select/index.js';
  import { Label } from '$lib/components/ui/label/index.js';
  import { Slider } from '$lib/components/ui/slider/index.js';
  import {
    LANGUAGES,
    GENDER_OPTIONS,
    ACCENT_OPTIONS,
    PITCH_OPTIONS,
    AGE_OPTIONS,
    STYLE_OPTIONS,
    UI_TEXT
  } from '$lib/tts/constants';
  let {
    lang = $bindable('en'),
    speed = $bindable(1.0),
    numStep = $bindable(32),
    selectedGender = $bindable('male'),
    selectedAccent = $bindable(''),
    selectedPitch = $bindable(''),
    selectedAge = $bindable(''),
    selectedStyle = $bindable(''),
    instruct = ''
  }: {
    lang?: string;
    speed?: number;
    numStep?: number;
    selectedGender?: string;
    selectedAccent?: string;
    selectedPitch?: string;
    selectedAge?: string;
    selectedStyle?: string;
    instruct?: string;
  } = $props();
</script>

<div class="space-y-4">
  <!-- Language -->
  <div class="space-y-1.5">
    <Label for="synth-lang">{UI_TEXT.language}</Label>
    <Select.Root bind:value={lang}>
      <Select.Trigger id="synth-lang" class="w-full">
        {LANGUAGES.find((o) => o.value === lang)?.label ?? 'Select language...'}
      </Select.Trigger>
      <Select.Content>
        {#each LANGUAGES as option (option.value)}
          <Select.Item value={option.value} label={option.label} />
        {/each}
      </Select.Content>
    </Select.Root>
  </div>

  <!-- Voice Characteristics 2-col grid -->
  <div class="grid grid-cols-2 gap-3">
    <!-- Gender -->
    <div class="space-y-1.5">
      <Label for="synth-gender">{UI_TEXT.gender}</Label>
      <Select.Root bind:value={selectedGender}>
        <Select.Trigger id="synth-gender" class="w-full">
          {GENDER_OPTIONS.find((o) => o.value === selectedGender)?.label ?? 'Any'}
        </Select.Trigger>
        <Select.Content>
          {#each GENDER_OPTIONS as option (option.value)}
            <Select.Item value={option.value} label={option.label} />
          {/each}
        </Select.Content>
      </Select.Root>
    </div>

    <!-- Accent -->
    <div class="space-y-1.5">
      <Label for="synth-accent">{UI_TEXT.accent}</Label>
      <Select.Root bind:value={selectedAccent}>
        <Select.Trigger id="synth-accent" class="w-full">
          {ACCENT_OPTIONS.find((o) => o.value === selectedAccent)?.label ?? 'Any'}
        </Select.Trigger>
        <Select.Content>
          {#each ACCENT_OPTIONS as option (option.value)}
            <Select.Item value={option.value} label={option.label} />
          {/each}
        </Select.Content>
      </Select.Root>
    </div>

    <!-- Pitch -->
    <div class="space-y-1.5">
      <Label for="synth-pitch">{UI_TEXT.pitch}</Label>
      <Select.Root bind:value={selectedPitch}>
        <Select.Trigger id="synth-pitch" class="w-full">
          {PITCH_OPTIONS.find((o) => o.value === selectedPitch)?.label ?? 'Any'}
        </Select.Trigger>
        <Select.Content>
          {#each PITCH_OPTIONS as option (option.value)}
            <Select.Item value={option.value} label={option.label} />
          {/each}
        </Select.Content>
      </Select.Root>
    </div>

    <!-- Age -->
    <div class="space-y-1.5">
      <Label for="synth-age">{UI_TEXT.age}</Label>
      <Select.Root bind:value={selectedAge}>
        <Select.Trigger id="synth-age" class="w-full">
          {AGE_OPTIONS.find((o) => o.value === selectedAge)?.label ?? 'Any'}
        </Select.Trigger>
        <Select.Content>
          {#each AGE_OPTIONS as option (option.value)}
            <Select.Item value={option.value} label={option.label} />
          {/each}
        </Select.Content>
      </Select.Root>
    </div>
  </div>

  <!-- Style -->
  <div class="space-y-1.5">
    <Label for="synth-style">{UI_TEXT.style}</Label>
    <Select.Root bind:value={selectedStyle}>
      <Select.Trigger id="synth-style" class="w-full">
        {STYLE_OPTIONS.find((o) => o.value === selectedStyle)?.label ?? 'Normal'}
      </Select.Trigger>
      <Select.Content>
        {#each STYLE_OPTIONS as option (option.value)}
          <Select.Item value={option.value} label={option.label} />
        {/each}
      </Select.Content>
    </Select.Root>
  </div>

  <!-- Current Instruct Preview -->
  {#if instruct}
    <div class="rounded-md border border-dashed border-zinc-700 bg-zinc-800/40 px-3 py-2">
      <p class="text-muted-foreground mb-1 text-xs font-medium uppercase tracking-wide">
        {UI_TEXT.currentInstruct}
      </p>
      <p class="text-foreground text-sm">{instruct}</p>
    </div>
  {/if}

  <!-- Speed -->
  <div class="space-y-2">
    <div class="flex items-center justify-between">
      <Label for="synth-speed">{UI_TEXT.speed}</Label>
      <span class="text-muted-foreground text-xs tabular-nums">{speed.toFixed(1)}</span>
    </div>
    <Slider id="synth-speed" min={0.5} max={2.0} step={0.1} bind:value={speed} class="w-full" />
  </div>

  <!-- Diffusion Steps -->
  <div class="space-y-2">
    <div class="flex items-center justify-between">
      <Label for="synth-steps">{UI_TEXT.diffusionSteps}</Label>
      <span class="text-muted-foreground text-xs tabular-nums">{numStep}</span>
    </div>
    <Slider id="synth-steps" min={4} max={64} step={4} bind:value={numStep} class="w-full" />
  </div>
</div>
