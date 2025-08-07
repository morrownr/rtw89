// SPDX-License-Identifier: GPL-2.0 OR BSD-3-Clause
/* Copyright(c) 2025  Realtek Corporation
 */

#include <linux/module.h>
#include <linux/usb.h>
#include "rtw8922a.h"
#include "usb.h"

static const struct rtw89_driver_info rtw89_8922au_info = {
	.chip = &rtw8922a_chip_info,
	.variant = NULL,
	.quirks = NULL,
};

static const struct usb_device_id rtw_8922au_id_table[] = {
	{ USB_DEVICE_AND_INTERFACE_INFO(0x0b05, 0x1bcf, 0xff, 0xff, 0xff),
	  .driver_info = (kernel_ulong_t)&rtw89_8922au_info },
	{ USB_DEVICE_AND_INTERFACE_INFO(0x0b05, 0x1bd2, 0xff, 0xff, 0xff),
	  .driver_info = (kernel_ulong_t)&rtw89_8922au_info },
	{ USB_DEVICE_AND_INTERFACE_INFO(0x0bda, 0x8912, 0xff, 0xff, 0xff),
	  .driver_info = (kernel_ulong_t)&rtw89_8922au_info },
	{ USB_DEVICE_AND_INTERFACE_INFO(0x0db0, 0xda0e, 0xff, 0xff, 0xff),
	  .driver_info = (kernel_ulong_t)&rtw89_8922au_info },
	{ USB_DEVICE_AND_INTERFACE_INFO(0x3625, 0x010a, 0xff, 0xff, 0xff),
	  .driver_info = (kernel_ulong_t)&rtw89_8922au_info },
	{ USB_DEVICE_AND_INTERFACE_INFO(0x7392, 0x3822, 0xff, 0xff, 0xff),
	  .driver_info = (kernel_ulong_t)&rtw89_8922au_info },
	{},
};
MODULE_DEVICE_TABLE(usb, rtw_8922au_id_table);

static struct usb_driver rtw_8922au_driver = {
	.name = KBUILD_MODNAME,
	.id_table = rtw_8922au_id_table,
	.probe = rtw89_usb_probe,
	.disconnect = rtw89_usb_disconnect,
};
module_usb_driver(rtw_8922au_driver);

MODULE_AUTHOR("Bitterblue Smith <rtl8821cerfe2@gmail.com>");
MODULE_DESCRIPTION("Realtek 802.11be wireless 8922AU driver");
MODULE_LICENSE("Dual BSD/GPL");
