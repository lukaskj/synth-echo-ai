import type { RequestStatus } from '$lib/tts/types';

type DashboardHeaderHandlers = {
  onLoadModel: (() => void | Promise<void>) | null;
  onUnloadModel: (() => void | Promise<void>) | null;
};

class DashboardHeaderState {
  status = $state<RequestStatus>('idle');
  modelReady = $state(false);
  modelDevice = $state<string | null>(null);
  isBusy = $state(false);
  handlers = $state<DashboardHeaderHandlers>({
    onLoadModel: null,
    onUnloadModel: null
  });

  setState(payload: {
    status: RequestStatus;
    modelReady: boolean;
    modelDevice: string | null;
    isBusy: boolean;
    onLoadModel: () => void | Promise<void>;
    onUnloadModel: () => void | Promise<void>;
  }) {
    this.status = payload.status;
    this.modelReady = payload.modelReady;
    this.modelDevice = payload.modelDevice;
    this.isBusy = payload.isBusy;
    this.handlers = {
      onLoadModel: payload.onLoadModel,
      onUnloadModel: payload.onUnloadModel
    };
  }

  reset() {
    this.status = 'idle';
    this.modelReady = false;
    this.modelDevice = null;
    this.isBusy = false;
    this.handlers = {
      onLoadModel: null,
      onUnloadModel: null
    };
  }
}

export const dashboardHeaderState = new DashboardHeaderState();
