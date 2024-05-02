import type { AxiosError, AxiosResponse, AxiosStatic } from "axios";

export const BaseError = {
    Network: "network",
    Unknown: "unknown",
} as const;

export function checkAxiosError<E extends { [key in keyof typeof BaseError]: string }, T = unknown>(
    axios: AxiosStatic,
    error: any
): (AxiosError<T> & { response: AxiosResponse<T> }) | E[keyof typeof BaseError] {
    if (!axios.isAxiosError<T>(error)) return BaseError.Unknown;
    if (error.response === undefined) return BaseError.Network;
    return error as AxiosError<T> & { response: AxiosResponse<T> };
}
