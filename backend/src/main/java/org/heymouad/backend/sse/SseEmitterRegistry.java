package org.heymouad.backend.sse;

import org.springframework.stereotype.Component;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.util.concurrent.ConcurrentHashMap;

@Component
public class SseEmitterRegistry {
    private final ConcurrentHashMap<String, SseEmitter> emitters = new ConcurrentHashMap<>();
    public void addEmitter(String id, SseEmitter emitter) { emitters.put(id, emitter); }
    public SseEmitter removeEmitter(String id) { return emitters.remove(id); }
    public SseEmitter getEmitter(String id) { return emitters.get(id); }
}