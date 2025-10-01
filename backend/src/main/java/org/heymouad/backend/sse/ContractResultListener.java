package org.heymouad.backend.sse;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.connection.Message;
import org.springframework.data.redis.connection.MessageListener;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.nio.charset.StandardCharsets;
import java.util.Map;

@Component
@RequiredArgsConstructor
@Slf4j
public class ContractResultListener implements MessageListener {
    private final SseEmitterRegistry emitterRegistry;

    @Override
    public void onMessage(Message message, byte[] pattern) {
        try {
            String body = new String(message.getBody(), StandardCharsets.UTF_8);
            Map<String, Object> map = new ObjectMapper().readValue(body, Map.class);
            String id = (String) map.get("id");
            String result = (String) map.get("result");
            SseEmitter emitter = emitterRegistry.removeEmitter(id);
            if (emitter != null) {
                emitter.send(result, MediaType.APPLICATION_JSON);
                emitter.complete();
            }
        } catch (Exception e) {
            log.error("Error processing contract result pubsub message", e);
        }
    }
}