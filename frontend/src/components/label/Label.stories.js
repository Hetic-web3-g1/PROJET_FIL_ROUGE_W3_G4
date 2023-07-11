import { Label } from './Label';

export default {
  title: 'Label',
  component: Label,
  tags: ['autodocs'],
  argTypes: {
    backgroundColor: { control: 'color' },
  },
};

export const InProgress = {
  args: {
    label: 'In progress',
    type: 'in-progress',
  },
};

export const Completed = {
  args: {
    label: 'Completed',
    type: 'completed',
  },
};

export const Archive = {
  args: {
    label: 'Archive',
    type: 'archive',
  },
};

export const Review = {
  args: {
    label: 'Review',
    type: 'review',
  },
};

