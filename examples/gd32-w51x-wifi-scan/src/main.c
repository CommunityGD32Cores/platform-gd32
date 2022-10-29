#include "gd32w51x.h"
#include "wrapper_os.h"
#include "wifi_netlink.h"
#include "app_type.h"
#include "wifi_management.h"
#include "arm_math.h"
#include "wifi_version.h"
#include "nspe_region.h"
#include "mbl_uart.h"

static void scan_info_print(struct wifi_scan_info *scan_item)
{
    DEBUGPRINT("----------------------------------------------------\r\n");
    DEBUGPRINT("SSID:        %s\r\n", &scan_item->ssid.ssid);
    DEBUGPRINT("Channel:     %d\r\n", scan_item->channel);
    switch (scan_item->encryp_protocol) {
    case WIFI_ENCRYPT_PROTOCOL_OPENSYS:
        DEBUGPRINT("Security:    Open\r\n");
        break;
    case WIFI_ENCRYPT_PROTOCOL_WEP:
        DEBUGPRINT("Security:    WEP\r\n");
        break;
    case WIFI_ENCRYPT_PROTOCOL_WPA:
        DEBUGPRINT("Security:    WPA\r\n");
        break;
    case WIFI_ENCRYPT_PROTOCOL_WPA2:
        DEBUGPRINT("Security:    WPA2\r\n");
        break;
    case WIFI_ENCRYPT_PROTOCOL_WPA3_TRANSITION:
        DEBUGPRINT("Security:    WPA2/WPA3\r\n");
        break;
    case WIFI_ENCRYPT_PROTOCOL_WPA3_ONLY:
        DEBUGPRINT("Security:    WPA3\r\n");
        break;
    default:
        DEBUGPRINT("Security:    Unknown\r\n");
        break;
    }

    if (scan_item->network_mode == WIFI_NETWORK_MODE_INFRA) {
        DEBUGPRINT("Network:     Infrastructure\r\n");
    } else if (scan_item->network_mode == WIFI_NETWORK_MODE_ADHOC) {
        DEBUGPRINT("Network:     Adhoc\r\n");
    } else {
        DEBUGPRINT("Network:     Unknown\r\n");
    }

    // bitrate_print(scan_item->rate);
    DEBUGPRINT("Rate:        %d Mbps\r\n", scan_item->rate);
    DEBUGPRINT("RSSI:        %d dbm\r\n", scan_item->rssi);
    DEBUGPRINT("BSSID:       "MAC_FMT"\r\n", MAC_ARG(scan_item->bssid_info.bssid));

    DEBUGPRINT("\r\n");
}

void cmd_cb_scan_done(void *eloop_data, void *user_ctx)
{
    DEBUGPRINT("[Scanned AP list]\r\n");

    wifi_netlink_scan_list_get(scan_info_print);

    eloop_event_unregister(WIFI_MGMT_EVENT_SCAN_DONE);
    eloop_event_unregister(WIFI_MGMT_EVENT_SCAN_FAIL);
}

void cmd_cb_scan_fail(void *eloop_data, void *user_ctx)
{
    DEBUGPRINT("WIFI_SCAN: failed\r\n");
    eloop_event_unregister(WIFI_MGMT_EVENT_SCAN_DONE);
    eloop_event_unregister(WIFI_MGMT_EVENT_SCAN_FAIL);
}

void start_task(void *p_arg) {
    sys_reset_flag_check();
    sys_os_misc_init();
    systick_delay_init();
    wifi_management_init();

    sys_ms_sleep(1000); // give WiFi task time to initialize

    DEBUGPRINT("Triggering WiFi scan NOW!\r\n");

    eloop_event_register(WIFI_MGMT_EVENT_SCAN_DONE, cmd_cb_scan_done, NULL, NULL);
    eloop_event_register(WIFI_MGMT_EVENT_SCAN_FAIL, cmd_cb_scan_fail, NULL, NULL);

    if (wifi_management_scan(FALSE) != 0) {
        eloop_event_unregister(WIFI_MGMT_EVENT_SCAN_DONE);
        eloop_event_unregister(WIFI_MGMT_EVENT_SCAN_FAIL);
        DEBUGPRINT("start wifi_scan failed\r\n");
    } else {
        DEBUGPRINT("WiFi scan started succesfully.\r\n");
    }

    // end of demo
    sys_task_delete(NULL);
}

int main(void)
{
    platform_init();

    DEBUGPRINT("SDK git revision: "WIFI_GIT_REVISION" \r\n");
    DEBUGPRINT("SDK version: V%d.%d.%d\r\n", (RE_NSPE_VERSION >> 24), ((RE_NSPE_VERSION & 0xFF0000) >> 16), (RE_NSPE_VERSION & 0xFFFF));
    DEBUGPRINT("SDK build date: " __DATE__ " " __TIME__" \r\n");

    sys_os_init();
    if (NULL == sys_task_create(NULL, (const uint8_t *)"start_task", NULL, START_TASK_STK_SIZE, 0,
            START_TASK_PRIO, start_task, NULL)) {
        DEBUGPRINT("ERROR: create start task failed\r\n");
    }
    sys_os_start();
    while(1);
    return 0;
}