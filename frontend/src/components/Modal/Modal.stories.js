import { Modal } from './Modal';

export default {
  title: 'Modal',
  component: Modal,
  tags: ['autodocs'],
  argTypes: {
    title: { control: 'text' },
    content: { control: 'text' },
    handleClose: { action: 'handleClose' },
  },
};

export const Default = {
    args: {
        title: 'Modal',
        content: 'This is a modal',
    },
};