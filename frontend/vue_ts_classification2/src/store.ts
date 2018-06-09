export const store = {
  debug: true,
  state: {
    message: 'Hello!',
    task: 'test task',
  },
  setMessageAction(newValue: string) {
    if (this.debug) {console.log('setMessageAction triggered with', newValue)};
    this.state.message = newValue;
  },
  clearMessageAction() {
    if (this.debug) {console.log('clearMessageAction triggered')};
    this.state.message = '';
  },
};