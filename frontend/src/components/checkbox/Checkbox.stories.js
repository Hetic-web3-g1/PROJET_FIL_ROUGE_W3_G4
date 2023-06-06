import { Checkbox } from './Checkbox';

export default {
  title: 'Checkbox',
  component: Checkbox
};

export const Base = {
  args: {
  },
};

export const Disabled = {
  args: {
    disabled: true
  },
};

export const CheckedByDefault = {
  args: {
  checkedByDefault: true,
  },
}

export const CheckedDisabled = {
  args: {
  checkedByDefault: true,
  disabled: true
  },
};

export const Secondary = {
  args: {
    primary: false,
  },
};
