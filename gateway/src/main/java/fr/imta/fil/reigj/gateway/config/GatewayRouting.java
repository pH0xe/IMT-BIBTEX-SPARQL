package fr.imta.fil.reigj.gateway.config;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class GatewayRouting {

    @Bean
    public RouteLocator configureRoute(RouteLocatorBuilder builder) {
        return builder.routes()
                .route("authModule", r -> r
                        .path("/auth/**")
//                        .filters(f -> f.filter(authFilter))
                        .uri("http://localhost:9000/")
                )
                .route("bibtexConvertModule", r-> r
                        .path("/api/bibtex/**")
//                        .filters(f -> f.filter(authFilter))
                        .uri("http://localhost:8081/")
                )
                .build();
    }
}
