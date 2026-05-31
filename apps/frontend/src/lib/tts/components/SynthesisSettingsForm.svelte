<script lang="ts">
  import {
    ACCENT_OPTIONS,
    AGE_OPTIONS,
    GENDER_OPTIONS,
    LANGUAGES,
    PITCH_OPTIONS,
    STYLE_OPTIONS,
    UI_TEXT
  } from '$lib/tts/constants';
  import RangeField from './RangeField.svelte';
  import SelectField from './SelectField.svelte';

  type Props = {
    synthesizeLang: string;
    synthesizeSpeed: number;
    synthesizeNumStep: number;
    selectedGender: string;
    selectedAccent: string;
    selectedPitch: string;
    selectedAge: string;
    selectedStyle: string;
    instruct: string;
  };

  let {
    synthesizeLang = $bindable(),
    synthesizeSpeed = $bindable(),
    synthesizeNumStep = $bindable(),
    selectedGender = $bindable(),
    selectedAccent = $bindable(),
    selectedPitch = $bindable(),
    selectedAge = $bindable(),
    selectedStyle = $bindable(),
    instruct
  }: Props = $props();
</script>

<SelectField
  id="language-select"
  label={UI_TEXT.language}
  options={LANGUAGES}
  bind:value={synthesizeLang}
/>

<div class="grid gap-4 sm:grid-cols-2">
  <SelectField
    id="gender-select"
    label={UI_TEXT.gender}
    options={GENDER_OPTIONS}
    bind:value={selectedGender}
  />
  <SelectField
    id="accent-select"
    label={UI_TEXT.accent}
    options={ACCENT_OPTIONS}
    bind:value={selectedAccent}
  />
  <SelectField
    id="pitch-select"
    label={UI_TEXT.pitch}
    options={PITCH_OPTIONS}
    bind:value={selectedPitch}
  />
  <SelectField id="age-select" label={UI_TEXT.age} options={AGE_OPTIONS} bind:value={selectedAge} />
  <div class="sm:col-span-2">
    <SelectField
      id="style-select"
      label={UI_TEXT.style}
      options={STYLE_OPTIONS}
      bind:value={selectedStyle}
    />
  </div>
</div>

<div class="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
  <p class="text-xs uppercase tracking-[0.18em] text-slate-500">{UI_TEXT.currentInstruct}</p>
  <p class="mt-3 text-base leading-7 text-slate-100">
    {#if instruct}
      {instruct}
    {:else}
      {UI_TEXT.noInstruction}
    {/if}
  </p>
</div>

<div class="grid gap-4 px-1">
  <RangeField
    id="speed-range"
    label={UI_TEXT.speed}
    displayValue={`${synthesizeSpeed.toFixed(1)}x`}
    min={0.5}
    max={2}
    step={0.1}
    bind:value={synthesizeSpeed}
  />

  <RangeField
    id="step-range"
    label={UI_TEXT.diffusionSteps}
    displayValue={`${synthesizeNumStep}`}
    min={8}
    max={64}
    step={8}
    bind:value={synthesizeNumStep}
  />
</div>
