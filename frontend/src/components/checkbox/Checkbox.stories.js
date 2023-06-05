import { Button } from './Button';

export default {
  title: 'Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    backgroundColor: { control: 'color' },
  },
};

export const White = {
  args: {
    primary: true,
    label: 'Button',
  },
};

export const Blue = {
  args: {
    label: 'Button',
  },
};

export const Medium = {
  args: {
    size: 'medium',
    label: 'Button',
  },
};

export const Small = {
  args: {
    size: 'small',
    label: 'Button',
  },
};